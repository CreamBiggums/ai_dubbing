import argparse
import os
import utils
import sys
import openai
from gtts import gTTS

openai_api_key = ''

def main():
    # Create header with authorization along with content-type
    header = {
        'authorization': 'd93f6f53b70b4e1aa83d2ab9b8f3572d',
        'content-type': 'application/json'
    }

    audioClip = input("Enter the name of audio file you wish to dub")

    audioClipFilePath = "audio_clips/" + audioClip

    upload_url = utils.upload_file(audioClipFilePath, header)

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

    audioTranslationFilePath = "audio_translations/" + audioClip + "es_com-mx.mp3"

    tts = gTTS(translated_transcript, lang='es', tld='com.mx')
    tts.save(audioTranslationFilePath)

    return


if __name__ == '__main__':
    main()
