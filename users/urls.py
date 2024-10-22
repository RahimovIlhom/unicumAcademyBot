from django.urls import path

from .views import stats_views, all_stats
from .views.users_views import ExportUsersToExcel, get_levels_for_telegram_user, SurveyCreateView, SurveyRetrieveView, \
    ExportSurveysToExcel


urlpatterns = [
    path('users/export/excel/', ExportUsersToExcel.as_view(), name='export_excel'),
    path('users/levels/bot-user/', get_levels_for_telegram_user, name='get_levels_for_telegram_user'),
    path('users/survey/create/', SurveyCreateView.as_view(), name='survey_create'),
    path('users/survey/<int:userId>/', SurveyRetrieveView.as_view(), name='survey_update'),
    path('users/export/survey/', ExportSurveysToExcel.as_view(), name='export_survey'),

    # path('survey-stats/age/', stats_views.AgeStatsAPIView.as_view(), name='age-stats'),
    # path('survey-stats/importance/', stats_views.ImportanceRankingStatsAPIView.as_view(), name='importance-stats'),
    # path('survey-stats/gender/', stats_views.GenderStatsAPIView.as_view(), name='gender-stats'),
    # path('survey-stats/course-number/', stats_views.CourseNumberStatsAPIView.as_view(), name='course-number-stats'),
    # path('survey-stats/education-type/', stats_views.EducationTypeStatsAPIView.as_view(), name='education-type-stats'),
    # path('survey-stats/education-direction/', stats_views.EducationDirectionStatsAPIView.as_view(),
    #      name='education-direction-stats'),
    # path('survey-stats/english-level/', stats_views.EnglishLevelStatsAPIView.as_view(), name='english-level-stats'),
    # path('survey-stats/english-goal/', stats_views.EnglishGoalStatsAPIView.as_view(), name='english-goal-stats'),
    # path('survey-stats/days-per-week/', stats_views.DaysPerWeekStatsAPIView.as_view(), name='days-per-week-stats'),
    # path('survey-stats/learning-experience/', stats_views.LearningExperienceStatsAPIView.as_view(),
    #      name='learning-experience-stats'),
    # path('survey-stats/obstacles/', stats_views.ObstacleStatsAPIView.as_view(), name='obstacles-stats'),
    # path('survey-stats/start-learning-importance/', stats_views.StartLearningImportanceStatsAPIView.as_view(),
    #      name='start-learning-importance-stats'),
    # path('survey-stats/english-proficiency/', stats_views.EnglishProficiencyStatsAPIView.as_view(),
    #      name='english-proficiency-stats'),
    # path('survey-stats/course-type/', stats_views.CourseTypeStatsAPIView.as_view(), name='course-type-stats'),
    # path('survey-stats/conditions/', stats_views.ConditionStatsAPIView.as_view(), name='conditions-stats'),
    # path('survey-stats/consider-enrollment/', stats_views.ConsiderEnrollmentStatsAPIView.as_view(),
    #      name='consider-enrollment-stats'),
    # path('survey-stats/free-lesson-participation/', stats_views.FreeLessonParticipationStatsAPIView.as_view(),
    #      name='free-lesson-participation-stats'),

    path('stats/survey-all/', all_stats.CombinedStatsAPIView().as_view())
]
