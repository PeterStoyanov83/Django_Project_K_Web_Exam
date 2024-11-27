import { Layout } from '../components/Layout'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"

export default function Contact() {
  return (
    <Layout>
      <h1 className="text-4xl font-bold mb-6">Contact Us</h1>
      <div className="max-w-2xl mx-auto">
        <form className="space-y-6">
          <div>
            <Label htmlFor="name">Name</Label>
            <Input id="name" placeholder="Your name" required />
          </div>
          <div>
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="Your email" required />
          </div>
          <div>
            <Label htmlFor="subject">Subject</Label>
            <Input id="subject" placeholder="Subject of your message" required />
          </div>
          <div>
            <Label htmlFor="message">Message</Label>
            <Textarea id="message" placeholder="Your message" rows={5} required />
          </div>
          <Button type="submit">Send Message</Button>
        </form>
      </div>
    </Layout>
  )
}

