# Experiments with interfaces in Python.

class PaymentProcessor:
    def pay(self, amount):
        raise NotImplementedError("Subclasses must implement pay()")


class CardProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Paid ${amount} with card"


class PaypalProcessor(PaymentProcessor):
    def pay(self, amount):
        return f"Paid ${amount} with PayPal"


class StripeProcessor(PaymentProcessor):
    pass


def checkout(processor: PaymentProcessor, amount):
    return processor.pay(amount)


card = CardProcessor()
paypal = PaypalProcessor()
stripe = StripeProcessor()
something = object()

print(checkout(card, 100))
print(checkout(paypal, 55))

# Will crash with NotImplementedError, because StripeProcessor is not implementing / overriding pay method.
# Hence - will call the one from PaymentProcessor.
print(checkout(stripe, 123))

# Will crash with AttributeError, because there is no pay method.
# print(checkout(something, 66))

# TODO: Other way of using interfaces in Python is with Use abc.ABC and @abstractmethod