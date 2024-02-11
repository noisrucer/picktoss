from reminder.domain.subscription.enum import SubscriptionPlanType

DOCUMENT_MAX_LEN = 15000

FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM = 3
PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM = 5


def get_max_document_num_by_subscription_plan(plan: SubscriptionPlanType) -> int:
    assert isinstance(plan, SubscriptionPlanType)

    if plan == SubscriptionPlanType.FREE:
        return FREE_PLAN_MONTHLY_MAX_DOCUMENT_NUM
    elif plan == SubscriptionPlanType.PRO:
        return PRO_PLAN_MONTHLY_MAX_DOCUMENT_NUM
    else:
        raise ValueError("invalid subscription plan type")
