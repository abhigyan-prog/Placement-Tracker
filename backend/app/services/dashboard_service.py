from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.user import User
from app.schemas.dashboard import DashboardResponse, StatusCount


def get_dashboard_stats(
    db: Session,
    current_user: User,
) -> DashboardResponse:

    status_result = db.execute(
        select(
            Application.status,
            func.count(Application.id)
        )
        .where(
            Application.user_id == current_user.id
        )
        .group_by(Application.status)
    )

    status_counts = {
        "applied": 0,
        "oa": 0,
        "interview": 0,
        "rejected": 0,
        "offer": 0,
    }

    for status, count in status_result:
        status_counts[status.value.lower()] = count

    by_status = StatusCount(**status_counts)

    total_applications = sum(status_counts.values())

    active_applications = (
        by_status.applied
        + by_status.oa
        + by_status.interview
    )

    offers_received = by_status.offer

    rejections = by_status.rejected

    success_rate = (
        (offers_received / total_applications) * 100
        if total_applications > 0
        else 0.0
    )

    today = date.today()
    start_of_month = today.replace(day=1)

    if today.month == 12:
        start_of_next_month = date(today.year + 1, 1, 1)
    else:
        start_of_next_month = date(today.year, today.month + 1, 1)

    applications_this_month = db.scalar(
        select(func.count(Application.id))
        .where(
            Application.user_id == current_user.id,
            Application.application_date >= start_of_month,
            Application.application_date < start_of_next_month,
        )
    )

    return DashboardResponse(
        total_applications=total_applications,
        active_applications=active_applications,
        offers_received=offers_received,
        rejections=rejections,
        success_rate=success_rate,
        applications_this_month=applications_this_month,
        by_status=by_status,
    )