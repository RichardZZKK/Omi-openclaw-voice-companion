import Foundation
import Speech
import AVFoundation

// Enable on-device recognition
SFSpeechRecognizer.requestAuthorization { status in
    guard status == .authorized else {
        print("Speech recognition not authorized")
        exit(1)
    }
}

guard let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US")) else {
    print("Speech recognizer not available")
    exit(1)
}

let fileURL = URL(fileURLWithPath: CommandLine.arguments[1])
let request = SFSpeechURLRecognitionRequest(url: fileURL)
request.shouldReportPartialResults = false
request.requiresOnDeviceRecognition = true

recognizer.recognitionTask(with: request) { result, error in
    if let result = result {
        print(result.bestTranscription.formattedString)
        exit(0)
    }
    if let error = error {
        print("Error: \(error)")
        exit(1)
    }
}

RunLoop.current.run(until: Date(timeIntervalSinceNow: 30))
