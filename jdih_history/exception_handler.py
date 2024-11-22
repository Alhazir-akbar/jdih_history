from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps DRF's default error responses
    into a consistent format:
    
    {
        "success": false,
        "message": "Detail error message",
        "data": null
    }
    """
    # Panggil handler default DRF terlebih dahulu
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            "success": False,
            "message": "",
            "data": None
        }

        # Memeriksa tipe data response
        if isinstance(response.data, dict):
            # Menggabungkan semua pesan error menjadi satu string
            messages = []
            for key, value in response.data.items():
                if isinstance(value, list):
                    messages.extend(value)
                else:
                    messages.append(str(value))
            custom_response["message"] = " ".join(messages)
        else:
            custom_response["message"] = str(response.data)

        # Menambahkan status code jika perlu (opsional)
        response.status_code = response.status_code  # Mempertahankan status code asli
        response.data = custom_response

    return response

def api_response(success=True, message="", data=None, status_code=200):
    """
    Fungsi utilitas untuk membuat respons API yang konsisten.
    
    Args:
        success (bool): Indikator keberhasilan.
        message (str): Pesan yang ingin disampaikan.
        data (dict): Data yang ingin disertakan dalam respons.
        status_code (int): Status HTTP.
    
    Returns:
        Response: DRF Response dengan struktur yang telah ditentukan.
    """
    return Response(
        {
            "success": success,
            "message": message,
            "data": data
        },
        status=status_code
    )