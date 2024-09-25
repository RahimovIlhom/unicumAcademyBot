import random

from asgiref.sync import sync_to_async, async_to_sync
from django.db import transaction
from django.db.models.functions import Random
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from tests.models import Question, TestSession, QuestionResponse
from tests.serializers import TestSessionResponseSerializer, TestSessionResultSerializer, TestSessionSerializer
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
        404: openapi.Response('Not found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)})),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def start_test_session(request):
    telegram_id = request.data.get('telegramId')
    level = request.data.get('level', '').lower()

    # Validate telegram ID
    if not telegram_id:
        return Response({'detail': 'Telegram ID is required'}, status=400)

    # Validate level
    valid_levels = [level[0] for level in LEVELS]
    if not level or level not in valid_levels:
        return Response({'detail': 'Invalid or missing level'}, status=400)

    # Fetch user
    user = get_object_or_404(BotUser, telegramId=telegram_id)

    # Update user's selected level
    user.selectedLevel = level
    user.save()

    # Retrieve random questions based on level (optimized)
    questions = Question.objects.filter(level=level).order_by(Random())[:20]

    # Ensure there are enough questions
    if not questions.exists():
        return Response({'detail': 'There are no questions for this level'}, status=404)

    # Create test session
    test_session, created = TestSession.active_objects.get_or_create(user=user, level=level, totalQuestions=len(questions))

    # Prepare the response data
    questions_data = [
        {
            'questionId': question.id,
            'question': question.question,
            'image': question.image.url if question.image else None,
            'options': random.sample([  # random.sample returns a shuffled copy
                {'value': question.a, 'key': 'a'},
                {'value': question.b, 'key': 'b'},
                {'value': question.c, 'key': 'c'},
                {'value': question.d, 'key': 'd'}
            ], 4)  # 4 to shuffle all options
        }
        for question in questions
    ]

    # Return response with test session and questions
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
        200: TestSessionResultSerializer(),
        400: openapi.Response('Bad Request', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)})),
        404: openapi.Response('Not found', openapi.Schema(type=openapi.TYPE_OBJECT, properties={'detail': openapi.Schema(type=openapi.TYPE_STRING)})),
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def completed_test_session(request):
    test_session_id = request.data.get('testSessionId')
    user_responses = request.data.get('userResponses')

    # Validate request data
    if not test_session_id:
        return Response({'detail': 'Test session ID is required'}, status=400)
    if not user_responses:
        return Response({'detail': 'User responses are required'}, status=400)

    # Fetch test session
    test_session = get_object_or_404(TestSession, id=test_session_id)

    if test_session.completed:
        return Response({'detail': 'Test session already completed'}, status=400)

    # Get all related questions at once for optimization
    question_ids = [response.get('questionId') for response in user_responses]
    questions = {q.id: q for q in Question.objects.filter(id__in=question_ids)}

    question_responses = []
    missing_questions = []  # Collect missing questions

    with transaction.atomic():  # Ensure atomic DB transactions
        for user_response in user_responses:
            question_id = user_response.get('questionId')
            answer = user_response.get('answer')

            # Validate and fetch question
            question = questions.pop(question_id, None)
            if not question:
                # Collect missing question IDs
                missing_questions.append(question_id)
                continue  # Skip to next response

            # Create question response object
            question_responses.append(QuestionResponse(
                user=test_session.user,
                question=question,
                test_session=test_session,
                answer=answer,
                correct=(answer == 'a')  # Assumed 'a' is correct; use actual logic
            ))

        # Bulk create all question responses
        QuestionResponse.objects.bulk_create(question_responses)

        # Mark test session as completed
        test_session.completed = True
        test_session.save()

    # Update correct answers or other relevant logic
    test_session.update_correct_answers()

    async_to_sync(recommending_level_to_user)(test_session.user, test_session)

    # Serialize the response
    resp = TestSessionSerializer(test_session)

    # Include missing question IDs in the response if any
    response_data = {
        'test_session': resp.data,
        'missing_questions': missing_questions
    }

    return Response(response_data, status=200)


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
