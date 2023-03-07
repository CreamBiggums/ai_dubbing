import argparse
import os
import utils
import sys
import openai
from gtts import gTTS

openai_api_key = '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'

def main():
    # Create header with authorization along with content-type
    header = {
        'authorization': 'd93f6f53b70b4e1aa83d2ab9b8f3572d',
        'content-type': 'application/json'
    }


    upload_url = utils.upload_file("basketball_clip.mp3", header)

    print ("uploaded audio file")
    # Request a transcription
    transcript_response = utils.request_transcript(upload_url, header)
    print ("requested transcription")

    # Create a polling endpoint that will let us check when the transcription is complete
    polling_endpoint = utils.make_polling_endpoint(transcript_response)
    print ("polling")

    # Wait until the transcription is complete
    utils.wait_for_completion(polling_endpoint, header)
    print ("waiting")

    # Request the paragraphs of the transcript
    paragraphs = utils.get_paragraphs(polling_endpoint, header)
    print ("getting paragraphs")

    transcript = ""

    # Save and print transcript
    with open('transcript.txt', 'w') as f:
        for para in paragraphs:
            transcript += para['text']
            f.write(para['text'] + '\n')

    print (transcript)

    prompt = "Translate this into Spanish \n\n" + transcript

    print (prompt)

    openai.api_key = openai_api_key
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.3,
      max_tokens=100,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0
    )

    print (response["choices"][0]["text"])

    translated_transcript = response["choices"][0]["text"]

    tts = gTTS(translated_transcript, lang='es', tld='com.mx')
    tts.save('spanish_mexico_translation_mavs_basketball.mp3')

    tts = gTTS(translated_transcript, lang='es', tld='es')
    tts.save('spanish_spain_translation_mavs_basketball.mp3')
    return


if __name__ == '__main__':
    main()
