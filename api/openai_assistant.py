import os
from openai import OpenAI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.conf import settings

# Your specific assistant ID
ASSISTANT_ID = "asst_LPbLYXPpj9CmyAXcmJ77AJm3"


@csrf_exempt
@require_http_methods(["POST"])
def chat_with_assistant(request):
    if not settings.OPENAI_API_KEY:
        return JsonResponse({
            'error': 'OpenAI API key is not configured. Please contact the administrator.',
            'type': 'configuration_error'
        }, status=500)

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        data = json.loads(request.body)
        user_message = data.get('message')
        thread_id = data.get('thread_id')

        if not thread_id:
            # Create a new thread for the conversation
            thread = client.beta.threads.create()
            thread_id = thread.id

        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message
        )

        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )

        # Wait for the completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break

        # Get the latest message from the assistant
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_messages = [msg for msg in messages if msg.role == "assistant"]

        if assistant_messages:
            latest_message = assistant_messages[0].content[0].text.value
            return JsonResponse({
                'message': latest_message,
                'thread_id': thread_id,
                'type': 'success'
            })
        else:
            return JsonResponse({
                'error': 'No response from assistant',
                'type': 'api_error'
            }, status=500)

    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'type': 'api_error'
        }, status=500)

