import { Metadata } from 'next'
import Link from 'next/link'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { CalendarDays, GraduationCap, Laptop, Users } from 'lucide-react'

export const metadata: Metadata = {
  title: 'Project K Dashboard',
  description: 'Dashboard for Project K',
}

export default function DashboardPage() {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-red-500">
      <header className="px-4 lg:px-6 h-14 flex items-center">
        <Link className="flex items-center justify-center" href="#">
          <GraduationCap className="h-6 w-6 text-white" />
          <span className="sr-only">Project K</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link className="text-sm font-medium hover:underline text-white" href="#">
            Clients
          </Link>
          <Link className="text-sm font-medium hover:underline text-white" href="#">
            Courses
          </Link>
          <Link className="text-sm font-medium hover:underline text-white" href="#">
            Resources
          </Link>
        </nav>
      </header>
      <main className="flex-1 py-12 px-4 md:px-6">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <Card className="bg-white/90 backdrop-blur-lg">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-2xl font-bold">Clients</CardTitle>
              <Users className="w-8 h-8 text-gray-500" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">128</div>
              <p className="text-sm text-gray-500">Total active clients</p>
            </CardContent>
          </Card>
          <Card className="bg-white/90 backdrop-blur-lg">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-2xl font-bold">Courses</CardTitle>
              <GraduationCap className="w-8 h-8 text-gray-500" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">24</div>
              <p className="text-sm text-gray-500">Active courses</p>
            </CardContent>
          </Card>
          <Card className="bg-white/90 backdrop-blur-lg">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-2xl font-bold">Resources</CardTitle>
              <Laptop className="w-8 h-8 text-gray-500" />
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold">96</div>
              <p className="text-sm text-gray-500">Available resources</p>
            </CardContent>
          </Card>
        </div>
        <Tabs defaultValue="upcoming" className="mt-12">
          <TabsList className="bg-white/50 backdrop-blur-lg">
            <TabsTrigger value="upcoming">Upcoming Courses</TabsTrigger>
            <TabsTrigger value="recent">Recent Clients</TabsTrigger>
          </TabsList>
          <TabsContent value="upcoming" className="bg-white/90 backdrop-blur-lg p-4 rounded-lg mt-4">
            <ul className="space-y-4">
              {[1, 2, 3].map((_, i) => (
                <li key={i} className="flex items-center space-x-4">
                  <CalendarDays className="w-6 h-6 text-gray-500" />
                  <div>
                    <h3 className="font-semibold">Advanced Python Programming</h3>
                    <p className="text-sm text-gray-500">Starts on July {15 + i}, 2023</p>
                  </div>
                </li>
              ))}
            </ul>
          </TabsContent>
          <TabsContent value="recent" className="bg-white/90 backdrop-blur-lg p-4 rounded-lg mt-4">
            <ul className="space-y-4">
              {[1, 2, 3].map((_, i) => (
                <li key={i} className="flex items-center space-x-4">
                  <Users className="w-6 h-6 text-gray-500" />
                  <div>
                    <h3 className="font-semibold">TechCorp Inc.</h3>
                    <p className="text-sm text-gray-500">Joined on July {10 - i}, 2023</p>
                  </div>
                </li>
              ))}
            </ul>
          </TabsContent>
        </Tabs>
        <div className="mt-12 text-center">
          <Button className="bg-white text-purple-600 hover:bg-purple-100">View All Data</Button>
        </div>
      </main>
      <footer className="py-6 px-4 md:px-6 text-center text-white">
        <p>© 2023 Project K. All rights reserved.</p>
      </footer>
    </div>
  )
}

