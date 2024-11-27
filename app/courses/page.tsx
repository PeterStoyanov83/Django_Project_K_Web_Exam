'use client'

import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const courses = [
  {
    id: 1,
    title: "Web Development Fundamentals",
    description: "Learn the basics of HTML, CSS, and JavaScript.",
    category: "Web Development",
    level: "Beginner",
    image: "/placeholder.svg?height=200&width=300"
  },
  {
    id: 2,
    title: "Data Science Essentials",
    description: "Explore data analysis, visualization, and machine learning.",
    category: "Data Science",
    level: "Intermediate",
    image: "/placeholder.svg?height=200&width=300"
  },
  {
    id: 3,
    title: "Mobile App Development",
    description: "Create apps for iOS and Android platforms.",
    category: "Mobile Development",
    level: "Advanced",
    image: "/placeholder.svg?height=200&width=300"
  },
  // Add more courses as needed
]

export default function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('')
  const [levelFilter, setLevelFilter] = useState('')

  const filteredCourses = courses.filter(course => 
    course.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
    (categoryFilter === '' || course.category === categoryFilter) &&
    (levelFilter === '' || course.level === levelFilter)
  )

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Our Courses</h1>
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <Input
          placeholder="Search courses..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="md:w-1/3"
        />
        <Select onValueChange={setCategoryFilter}>
          <SelectTrigger className="md:w-1/3">
            <SelectValue placeholder="Filter by category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All Categories</SelectItem>
            <SelectItem value="Web Development">Web Development</SelectItem>
            <SelectItem value="Data Science">Data Science</SelectItem>
            <SelectItem value="Mobile Development">Mobile Development</SelectItem>
          </SelectContent>
        </Select>
        <Select onValueChange={setLevelFilter}>
          <SelectTrigger className="md:w-1/3">
            <SelectValue placeholder="Filter by level" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All Levels</SelectItem>
            <SelectItem value="Beginner">Beginner</SelectItem>
            <SelectItem value="Intermediate">Intermediate</SelectItem>
            <SelectItem value="Advanced">Advanced</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {filteredCourses.map((course) => (
          <Card key={course.id}>
            <CardHeader>
              <img src={course.image} alt={course.title} className="w-full h-48 object-cover rounded-t-lg" />
            </CardHeader>
            <CardContent>
              <CardTitle className="mb-2">{course.title}</CardTitle>
              <p className="mb-2">{course.description}</p>
              <p className="text-sm text-gray-600">Category: {course.category}</p>
              <p className="text-sm text-gray-600">Level: {course.level}</p>
            </CardContent>
            <CardFooter>
              <Button className="w-full">Enroll Now</Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}

