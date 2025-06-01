def populate_form_from_user(form, user):
    form.username.data = user.username
    form.email.data = user.email
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.is_active.data = user.is_active

def classify_moisture(controllers):
    stats = {'low': 0, 'medium': 0, 'good': 0}
    for controller in controllers:
        if controller.moisture_level < 30:
            stats['low'] += 1
        elif controller.moisture_level < 60:
            stats['medium'] += 1
        else:
            stats['good'] += 1
    return stats
