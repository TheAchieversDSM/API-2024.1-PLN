from pydantic import BaseModel


class Review(BaseModel):
    submission_date: str
    reviewer_id: str
    product_id: str
    product_name: str
    product_brand: str
    site_category_lv1: str
    site_category_lv2: str
    review_title: str
    overall_rating: str
    recommend_to_a_friend: str
    review_text: str
    reviewer_birth_year: str
    reviewer_gender: str
    reviewer_state: str
