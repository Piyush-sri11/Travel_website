from .models import Payment

class PaymentService:
    def process_payment(self, booking, amount):
        # Dummy payment processing logic
        payment_status = 'SUCCESS'  # In a real system, this would be determined by the payment gateway response
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_status=payment_status
        )
        return payment

    def process_refund(self, booking, amount):
        # Dummy refund processing logic
        refund_status = 'SUCCESS'  # In a real system, this would be determined by the payment gateway response
        payment = Payment.objects.get(booking=booking)
        payment.amount = amount
        payment.payment_status = refund_status
        payment.save()
        return payment