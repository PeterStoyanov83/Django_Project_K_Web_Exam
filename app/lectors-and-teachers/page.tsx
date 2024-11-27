import { NavBar } from '@/components/NavBar'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

const teachers = [
  { name: "Dr. Jane Smith", role: "Web Development", avatar: "/placeholder.svg?height=100&width=100" },
  { name: "Prof. John Doe", role: "Data Science", avatar: "/placeholder.svg?height=100&width=100" },
  { name: "Ms. Emily Johnson", role: "Mobile App Development", avatar: "/placeholder.svg?height=100&width=100" },
  { name: "Mr. Michael Brown", role: "UI/UX Design", avatar: "/placeholder.svg?height=100&width=100" },
]

export default function LectorsAndTeachersPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <NavBar />
      <main className="container mx-auto px-4 py-8 flex-grow">
        <h1 className="text-3xl font-bold mb-8">Our Lectors and Teachers</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {teachers.map((teacher, index) => (
            <Card key={index}>
              <CardHeader>
                <Avatar className="w-24 h-24 mx-auto">
                  <AvatarImage src={teacher.avatar} alt={teacher.name} />
                  <AvatarFallback>{teacher.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                </Avatar>
              </CardHeader>
              <CardContent className="text-center">
                <CardTitle className="mb-2">{teacher.name}</CardTitle>
                <p className="text-sm text-gray-600">{teacher.role}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  )
}

