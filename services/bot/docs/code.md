
'''py
if not display_galleries:
    buttons.append(
        InlineKeyboardButton(
            text=billboard, callback_data=atrium_callback_data
        )
    )
else:
    buttons.append(
        InlineKeyboardButton(
            text=atrium.selfButtonLabel,
            callback_data=atrium_callback_data,
        )
    )
# * --/Galleries
galleries = theater.galleries

for gallery in galleries:
    buttons.append(
        InlineKeyboardButton(
            text=gallery.selfButtonLabel,
            callback_data=f"@{theater_id}://{gallery.name}",
        )
    )
'''