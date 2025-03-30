import json
import os

import requests


def main(context):
    # Parse the request data
    try:
        data = json.loads(context.req.body)
        images = data.get("images", [])
        longitude = data.get("longitude")
        latitude = data.get("latitude")

        if not images or longitude is None or latitude is None:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "error": "Missing required parameters: images, longitude, or latitude"
                    }
                ),
            }

        # Your Plant.id API key should be set as an environment variable in the Appwrite function
        api_key = os.environ.get("PLANT_ID_API_KEY")
        if not api_key:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "API key not configured"}),
            }

        # Prepare the request to Plant.id API
        plant_id_url = "https://plant.id/api/v3/health_assessment"

        # For each base64 image, make sure it has the correct prefix
        formatted_images = []
        for img in images:
            # Check if the image already has the data:image prefix
            if not img.startswith("data:image"):
                img = "data:image/jpeg;base64," + img
            formatted_images.append(img)

        payload = {
            "images": formatted_images,
            "latitude": latitude,
            "longitude": longitude,
            "similar_images": True,
        }

        headers = {"Api-Key": api_key, "Content-Type": "application/json"}

        # Make the request to Plant.id API
        response = requests.post(plant_id_url, headers=headers, json=payload)

        # Return the response
        return {"statusCode": response.status_code, "body": response.text}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
