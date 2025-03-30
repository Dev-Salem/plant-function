import json
import os

import requests


def main(context):
    context.log("Function started processing request")
    # Parse the request data
    try:
        context.log("Parsing request body")
        data = json.loads(context.req.body)
        images = data.get("images", [])
        longitude = data.get("longitude")
        latitude = data.get("latitude")
        context.log(
            f"Received request with {len(images)} images, longitude: {longitude}, latitude: {latitude}"
        )

        if not images or longitude is None or latitude is None:
            context.log("Missing required parameters, returning 400")
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "error": "Missing required parameters: images, longitude, or latitude"
                    }
                ),
            }

        # Your Plant.id API key should be set as an environment variable in the Appwrite function
        context.log("Retrieving Plant.id API key")
        api_key = os.environ.get("PLANT_ID_API_KEY")
        if not api_key:
            context.log("API key not configured, returning 500")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "API key not configured"}),
            }

        # Prepare the request to Plant.id API
        context.log("Preparing request to Plant.id API")
        plant_id_url = "https://crop.kindwise.com/api/v1/identification"

        # For each base64 image, make sure it has the correct prefix
        formatted_images = []
        for i, img in enumerate(images):
            context.log(f"Processing image {i+1}/{len(images)}")
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
        context.log("Sending request to Plant.id API")
        response = requests.post(plant_id_url, headers=headers, json=payload)
        context.log(
            f"Received response from Plant.id API with status code: {response.status_code}"
        )

        # Return the response
        context.log("Returning response to client")
        return {"statusCode": response.status_code, "body": response.text}

    except Exception as e:
        context.log(f"Error occurred: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
