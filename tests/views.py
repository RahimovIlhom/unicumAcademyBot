from asgiref.sync import async_to_sync, sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from tests.models import Question, TestSession, QuestionResponse
from tests.serializers import TestSessionResponseSerializer, TestSessionSerializer
from users.models import BotUser, LEVELS
from users.utils.data import LEVELS_DICT, LEVELS_LIST

start_test_session_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'telegramId': openapi.Schema(type=openapi.TYPE_STRING, description="Telegram ID of the user"),
        'level': openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Level of the questions",
            enum=[level[0] for level in LEVELS]
        ),
    },
    required=['telegramId', 'level']
)

@swagger_auto_schema(
    method='post',
    request_body=start_test_session_schema,
    responses={
        201: TestSessionResponseSerializer(),
        400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)})),
        404: 'Telegram ID not found',
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def start_test_session(request):
    telegram_id = request.data.get('telegramId')
    level = request.data.get('level')

    if not telegram_id:
        return Response({'detail': 'Telegram ID not found'}, status=400)

    if not level:
        return Response({'detail': 'Level not found'}, status=400)
    else:
        if level not in [level[0] for level in LEVELS]:
            return Response({'detail': 'Invalid level'}, status=400)

    user = get_object_or_404(BotUser, telegramId=telegram_id)
    user.selectedLevel = level
    user.save()

    questions = Question.objects.filter(level=level).order_by('?')[:20]

    if not questions:
        return Response({'detail': 'No questions found'}, status=404)

    test_session = TestSession.objects.create(user=user, level=level, totalQuestions=len(questions))

    questions_data = [
        {
            'id': question.id,
            'question': question.question,
            'image': question.image.url if question.image else None,
            'options':[
                {
                    'value': question.a,
                    'key': 'a'
                },
                {
                    'value': question.b,
                    'key': 'b'
                },
                {
                    'value': question.c,
                    'key': 'c'
                },
                {
                    'value': question.d,
                    'key': 'd'
                }
            ]
        } for question in questions
    ]

    return Response({
        'testSessionId': test_session.id,
        'questions': questions_data,
        'totalQuestions': len(questions)
    }, status=201)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'testSessionId': openapi.Schema(type=openapi.TYPE_NUMBER, description="Test session ID"),
            'userResponses': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'questionId': openapi.Schema(type=openapi.TYPE_NUMBER, description="Question ID"),
                        'answer': openapi.Schema(type=openapi.TYPE_STRING, description="Answer", enum=['a', 'b', 'c', 'd']),
                    },
                    required=['questionId', 'answer']
                ),
            ),
        },
        required=['testSessionId', 'userResponses']
    ),
    responses={
        200: TestSessionSerializer(),
        400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)})),
        404: openapi.Response('Test session not found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)})),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def completed_test_session(request):
    test_session_id = request.data.get('testSessionId')
    user_responses = request.data.get('userResponses')

    if not test_session_id:
        return Response({'detail': 'Test session ID not found'}, status=400)

    test_session = get_object_or_404(TestSession, id=test_session_id)
    if test_session.completed:
        return Response({'detail': 'Test session already completed'}, status=404)

    for user_response in user_responses:
        question_id = user_response.get('questionId')
        answer = user_response.get('answer')
        question = get_object_or_404(Question, id=question_id)
        question_response = QuestionResponse.objects.create(
            user=test_session.user,
            question=question,
            test_session=test_session,
            answer=answer,
            correct=answer == 'a'
        )
        question_response.save()

    test_session.completed = True
    test_session.save()

    test_session.update_correct_answers()

    async_to_sync(recommending_level_to_user)(test_session.user, test_session)

    resp = TestSessionSerializer(test_session)
    return Response(resp.data, status=200)


async def recommending_level_to_user(user: BotUser, test_session: TestSession):
    totalQuestions = test_session.totalQuestions
    correctAnswers = test_session.correctAnswers

    result_percentage = (correctAnswers / totalQuestions) * 100

    if result_percentage >= 90:
        user.confirmedLevel = test_session.level
        user.recommendedLevel = LEVELS_LIST[LEVELS_DICT[test_session.level] + 1 if test_session.level != 'advanced' else 5]
    elif result_percentage >= 75:
        user.confirmedLevel = test_session.level
        user.recommendedLevel = test_session.level
    else:
        user.recommendedLevel = LEVELS_LIST[LEVELS_DICT[test_session.level] - 1 if test_session.level != 'beginner' else 0]

    await sync_to_async(user.save)()
