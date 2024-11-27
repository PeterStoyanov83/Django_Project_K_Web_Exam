'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { MessageCircle } from 'lucide-react'
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"

export function ChatbotButton() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <Sheet open={isOpen} onOpenChange={setIsOpen}>
        <SheetTrigger asChild>
          <Button size="lg" className="rounded-full w-16 h-16">
            <MessageCircle className="h-8 w-8" />
            <span className="sr-only">Open AI Chatbot</span>
          </Button>
        </SheetTrigger>
        <SheetContent side="right" className="w-[400px] sm:w-[540px]">
          <SheetHeader>
            <SheetTitle>AI Chatbot</SheetTitle>
            <SheetDescription>
              Ask any questions about Project K
            </SheetDescription>
          </SheetHeader>
          <div className="mt-4">
            {/* Placeholder for AI chatbot integration */}
            <p>AI chatbot will be integrated here.</p>
          </div>
        </SheetContent>
      </Sheet>
    </div>
  )
}

