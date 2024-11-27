import { Layout } from '../components/Layout'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export default function Courses() {
  const courses = [
    { id: 1, name: "Web Development Fundamentals", description: "Learn the basics of HTML, CSS, and JavaScript.", platform: "Online" },
    { id: 2, name: "Data Science Essentials", description: "Explore data analysis, visualization, and machine learning.", platform: "In-Person" },
    { id: 3, name: "Mobile App Development", description: "Create apps for iOS and Android platforms.", platform: "Online" },
    { id: 4, name: "UI/UX Design Principles", description: "Master the art of creating user-friendly interfaces.", platform: "Online" },
  ]

  return (
    <Layout>
      <h1 className="text-4xl font-bold mb-6">Our Courses</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {courses.map((course) => (
          <Card key={course.id}>
            <CardHeader>
              <CardTitle>{course.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{course.description}</p>
              <p className="mt-2"><strong>Platform:</strong> {course.platform}</p>
            </CardContent>
            <CardFooter>
              <Button>View Course</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </Layout>
  )
}

