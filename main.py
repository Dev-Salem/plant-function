import json

import requests
from appwrite.client import Client
from appwrite.exception import AppwriteException
from appwrite.input_file import InputFile
from appwrite.services.storage import Storage


def lambda_handler(req, res):
    """
    Appwrite Function handler for Plant.id health assessment API integration
    """
    # Get request data
    try:
        data = req.json

        # Check if required parameters are provided
        if not data.get("images"):
            return res.json(
                {"success": False, "message": "No image data provided"}, 400
            )

        # Set default coordinates if not provided
        latitude = data.get("latitude", 0)
        longitude = data.get("longitude", 0)
        similar_images = data.get("similar_images", True)

        # Your Plant.id API key - in production, use environment variables
        api_key = req.env.get("PLANT_ID_API_KEY", "")

        if not api_key:
            return res.json(
                {"success": False, "message": "API key not configured"}, 500
            )

        # Prepare request to Plant.id API
        plant_id_url = "https://plant.id/api/v3/health_assessment"

        # Prepare the request payload
        payload = {
            "images": data.get("images"),
            "latitude": latitude,
            "longitude": longitude,
            "similar_images": similar_images,
        }

        # Set headers
        headers = {"Api-Key": api_key, "Content-Type": "application/json"}

        # Make the request to Plant.id API
        plant_id_response = requests.post(plant_id_url, headers=headers, json=payload)

        # Check if the request was successful
        if plant_id_response.status_code == 200:
            # Return the Plant.id API response
            return res.json({"success": True, "data": plant_id_response.json()})
        else:
            # Return error message
            return res.json(
                {
                    "success": False,
                    "message": "Error from Plant.id API",
                    "status_code": plant_id_response.status_code,
                    "response": plant_id_response.text,
                },
                plant_id_response.status_code,
            )

    except Exception as e:
        # Handle any unexpected errors
        return res.json(
            {"success": False, "message": f"Error processing request: {str(e)}"}, 500
        )


def main(context):
    """
    Entry point for the Appwrite function

    Args:
        context: The Appwrite function context containing request and response objects

    Returns:
        The result of the lambda_handler function
    """
    try:
        # Call the lambda handler with the request and response objects from the context
        return lambda_handler(context.req, context.res)
    except Exception as e:
        # Handle any unexpected errors at the top level
        return context.res.json(
            {"success": False, "message": f"Unhandled exception in main: {str(e)}"}, 500
        )
