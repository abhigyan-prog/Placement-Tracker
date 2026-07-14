from pydantic import BaseModel


class StatusCount(BaseModel):
    applied: int
    oa: int
    interview: int
    rejected: int
    offer: int


class DashboardResponse(BaseModel):
    total_applications: int
    active_applications: int
    offers_received: int
    rejections: int
    success_rate: float
    applications_this_month: int
    by_status: StatusCount
