from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.models import db as models
from app.settings import settings


async def send_email(ingredient: models.Ingredient):
    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=settings.MERCHANT_EMAIL,
        subject=f"Ingredient {ingredient.name} dropped to 50%",
        html_content=f"<strong>{ingredient.name} dropped to {ingredient.stock_quantity/1000} KG</strong>",
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(f"Error sending email: {e}")
