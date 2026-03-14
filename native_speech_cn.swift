import Foundation
import Speech
import AVFoundation

guard let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "zh-CN")) else {
    print("Speech recognizer not available for zh-CN")
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
