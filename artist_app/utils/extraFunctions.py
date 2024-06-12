from artist_app.models.appNotificationModel import AppNotificationModel

def add_notification_func(user, notification_type, title, booking_id):
        AppNotificationModel.objects.create(
            user_id=user,
            notification_type=notification_type,
            title=title,
            booking_id_id=booking_id
        )
        return None