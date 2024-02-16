from reminder.domain.subscription.enum import SubscriptionPlanType

DOCUMENT_MAX_LEN = 15000
DOCUMENT_MIN_LEN = 500

# 현재 구독 사이클에 업로드할 수 있는 문서 최대 개수
FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM = 15
PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM = 40

# 매 시점에 업로드될 수 있는 문서 최대 개수
FREE_PLAN_CURRENT_MAX_DOCUMENT_NUM = 10
PRO_PLAN_CURRENT_MAX_DOCUMENT_NUM = 40


def get_current_subscription_max_document_num_by_subscription_plan(plan: SubscriptionPlanType) -> int:
    assert isinstance(plan, SubscriptionPlanType)

    if plan == SubscriptionPlanType.FREE:
        return FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM
    elif plan == SubscriptionPlanType.PRO:
        return PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM
    else:
        raise ValueError("Invalid subscription plan type")


def get_anytime_max_document_num_by_subscription_plan(plan: SubscriptionPlanType) -> int:
    assert isinstance(plan, SubscriptionPlanType)

    if plan == SubscriptionPlanType.FREE:
        return FREE_PLAN_CURRENT_MAX_DOCUMENT_NUM
    elif plan == SubscriptionPlanType.PRO:
        return PRO_PLAN_CURRENT_MAX_DOCUMENT_NUM
    else:
        raise ValueError("Invalid subscription plan type")
