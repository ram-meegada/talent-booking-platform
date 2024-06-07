GENDER_CHOICES = [
    (1, "MALE"),
    (2, "FEMALE")
]

EXPERIENCE_CHOICES = [
    (1, "0-6 months"),
    (2, "6 months to 1 year"),
    (3, "1+ years"),
    (4, "2+ years"),
    (5, "3+ years"),
    (6, "4+ years"),
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
    (6, "MARKED COMPLETED"),
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
    (11,"Setting"),
    (12,"Logout"),
]

MODULE_PATHS = {
    1: '/dashboard',
    2: '/customers',
    3: '/artist',
    4: '/category',
    5: '/bookings',
    6: '/revenue',
    7: '/notification',
    8: '/reports',
    9: '/review',
    10: '/cms',
    11: '/setting',
    12: ''
}

NOTIFICATION_TYPE_CHOICES = [
    (1, "OFFER ACCEPTED"),
    (2, "OFFER CANCELLED BY TALENT"),
    (3, "TRANSACTION SUCCESS BY CLIENT"),
    (4, "PAYMENT RECEIVED BY CLIENT"),
    (4, "OFFER CANCELLED BY TALENT"),
]

FILTER_KEYS = {
    "experience": "user__experience__in", 
    "categories": "categories__overlap",
    "sub_categories": "sub_categories__overlap",
    "gender": "user__gender",
    "hair_color": "hair_color",
    "eye_color": "eye_color",
    "height_feet": "height_feet",
    "height_inches": "height_inches",
    "weight": "weight__range",
    "bust": "bust__range",
    "waist": "waist__range",
    "hips": "hips__range",
    "nationality": "user__country",
    "tags": "tags__overlap",
    "city": "user__city__icontains",
    "state": "user__state__icontains",
    "rating": "user__average_rating__gte",
    "booking_method": "booking_method__overlap"
    }