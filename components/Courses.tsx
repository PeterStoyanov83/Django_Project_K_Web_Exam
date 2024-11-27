import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

export function Courses() {
  const courses = [
    {
      title: "Web Development Fundamentals",
      description: "Learn the basics of HTML, CSS, and JavaScript.",
      image: "/placeholder.svg?height=200&width=300"
    },
    {
      title: "Data Science Essentials",
      description: "Explore data analysis, visualization, and machine learning.",
      image: "/placeholder.svg?height=200&width=300"
    },
    {
      title: "Mobile App Development",
      description: "Create apps for iOS and Android platforms.",
      image: "/placeholder.svg?height=200&width=300"
    }
  ]

  return (
    <section id="courses" className="py-20">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">Our Courses</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {courses.map((course, index) => (
            <Card key={index}>
              <CardHeader>
                <img src={course.image} alt={course.title} className="w-full h-48 object-cover rounded-t-lg" />
              </CardHeader>
              <CardContent>
                <CardTitle className="mb-2">{course.title}</CardTitle>
                <p>{course.description}</p>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Enroll Now</Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

