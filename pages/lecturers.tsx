import { Layout } from '../components/Layout'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const lecturers = [
  { name: "Dr. Jane Smith", specialization: "Web Development", avatar: "/placeholder.svg?height=100&width=100" },
  { name: "Prof. John Doe", specialization: "Data Science", avatar: "/placeholder.svg?height=100&width=100" },
  { name: "Dr. Emily Johnson", specialization: "Mobile App Development", avatar: "/placeholder.svg?height=100&width=100" },
  { name: "Prof. Michael Brown", specialization: "UI/UX Design", avatar: "/placeholder.svg?height=100&width=100" },
]

export default function Lecturers() {
  return (
    <Layout>
      <h1 className="text-4xl font-bold mb-8">Our Lecturers</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {lecturers.map((lecturer, index) => (
          <Card key={index}>
            <CardHeader>
              <Avatar className="w-24 h-24 mx-auto">
                <AvatarImage src={lecturer.avatar} alt={lecturer.name} />
                <AvatarFallback>{lecturer.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
              </Avatar>
            </CardHeader>
            <CardContent className="text-center">
              <CardTitle className="mb-2">{lecturer.name}</CardTitle>
              <p className="text-sm text-gray-600">{lecturer.specialization}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </Layout>
  )
}

