GENDER_CHOICES = [
    (1, "MALE"),
    (2, "FEMALE")
]

ROLE_CHOICE =[
    (1, "CLIENT"),
    (2, "TALENT"),
    (3, "ADMIN"),
    (4, "SUB ADMIN"),
]

HAIR_COLOR_CHOICES = [
    (1, "BROWN"),
    (2, "BLACK"),
    (3, "GRAY"),
    (4, "RED"),
]

EYE_COLOR_CHOICES = [
    (1, "BROWN"),
    (2, "BLACK"),
    (3, "GRAY"),
    (4, "GREEN"),
]

BOOKING_METHOD_CHOICES = [
    (1, "PRE BOOK"),
    (2, "PAY LATER"),
]

PROFILE_STATUS_CHOICES = [
    (1, "SIGN_UP_COMPLETED"),
    (2, "CATEGORIES ADDED"),
    (3, "MODEL STATUS ADDED"),
    (4, "PORTFOLIO ADDED"),
    (5, "BOOKING METHOD ADDED"),
]

VERIFICATION_STATUS_CHOICES = [
    (0, "PENDING"),
    (1, "ACCEPTED"),
    (2, "REJECTED"),
]

ADDRESS_CHOICE = [
    (1,"HOME"),
    (2,"WORK"),
    (3,"OTHER"),
]


BOOKING_STATUS = [
    (1,"PENDING"),
    (2,"COMPLETED"),
    (3,"CANCELLED"),
]

TRACK_BOOKING = [
    (1, "CLIENT MADE OFFER"),
    (2, "TALENT COUNTER OFFERED"),
    (3, "TALENT AND CLIENT BOTH ACCEPTED"),
    (4, "TALENT REJECTED"),
    (5, "CLIENT REJECTED"),
]

MODULE_CHOICES = [
    (1,"Dashboard"),
    (2,"Manage customers"),
    (3,"Manage artist"),
    (4,"Manage Category"),
    (5,"Booking Management"),
    (6,"Revenue Management"),
    (7,"Notification Management"),
    (8,"Report Management"),
    (9,"Manage Reviews"),
    (10,"Manage CMS"),
]