import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Mic, MicOff } from 'lucide-react';

interface VoiceInputProps {
  onTranscript: (text: string) => void;
}

export default function VoiceInput({ onTranscript }: VoiceInputProps) {
  const [isRecording, setIsRecording] = useState(false);
  
  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Voice input não suportado neste navegador');
      return;
    }
    
    if (isRecording) {
      setIsRecording(false);
      // Stop recording
      return;
    }
    
    setIsRecording(true);
    
    // @ts-ignore - Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    recognition.lang = 'pt-BR';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onTranscript(transcript);
      setIsRecording(false);
    };
    
    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      setIsRecording(false);
    };
    
    recognition.onend = () => {
      setIsRecording(false);
    };
    
    recognition.start();
  };
  
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={handleVoiceInput}
      className={isRecording ? 'bg-red-100 border-red-500' : ''}
      title="Voice input (Web Speech API)"
    >
      {isRecording ? (
        <MicOff className="w-4 h-4 text-red-600" />
      ) : (
        <Mic className="w-4 h-4" />
      )}
    </Button>
  );
}


