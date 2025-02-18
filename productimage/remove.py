import requests
# real image path
image = "media/product_images/479729040_608315328829052_8506768532072163407_n.jpg"
image_name = "479729040_608315328829052_8506768532072163407_n.jpg"
image_file = open(image, 'rb')
if image:
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_file},
        data={'size': 'auto'},
        headers={'X-Api-Key': ''},
    )
    if response.status_code == requests.codes.ok:
        with open(f'{image_name}-no-bg.png', 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)
