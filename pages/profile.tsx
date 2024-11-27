import { Layout } from '../components/Layout'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

// This data should come from your backend, based on the Models.py
const userData = {
  name: "John Doe",
  email: "john.doe@example.com",
  location: "New York",
  agreementStatus: true,
  courses: [
    { name: "Web Development Fundamentals", platform: "Online" },
    { name: "Data Science Essentials", platform: "In-Person" },
  ],
  laptops: [
    { identifier: "LAP-12345", assignedDate: "2023-01-15", returnDate: "2023-12-31" },
  ],
}

export default function Profile() {
  return (
    <Layout>
      <h1 className="text-4xl font-bold mb-6">My Profile</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
          </CardHeader>
          <CardContent>
            <Avatar className="w-24 h-24 mx-auto mb-4">
              <AvatarImage src="/placeholder.svg?height=100&width=100" alt={userData.name} />
              <AvatarFallback>{userData.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
            </Avatar>
            <p><strong>Name:</strong> {userData.name}</p>
            <p><strong>Email:</strong> {userData.email}</p>
            <p><strong>Location:</strong> {userData.location}</p>
            <p><strong>Agreement Status:</strong> {userData.agreementStatus ? 'Active' : 'Inactive'}</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Enrolled Courses</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside">
              {userData.courses.map((course, index) => (
                <li key={index}>{course.name} ({course.platform})</li>
              ))}
            </ul>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Assigned Laptops</CardTitle>
          </CardHeader>
          <CardContent>
            {userData.laptops.map((laptop, index) => (
              <div key={index} className="mb-4">
                <p><strong>Identifier:</strong> {laptop.identifier}</p>
                <p><strong>Assigned Date:</strong> {laptop.assignedDate}</p>
                <p><strong>Return Date:</strong> {laptop.returnDate}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </Layout>
  )
}

