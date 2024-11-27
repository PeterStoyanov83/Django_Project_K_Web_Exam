'use client'

import Link from 'next/link'
import { useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet"
import { BookOpen, Users, Home } from 'lucide-react'

type User = {
  name: string;
  role: 'student' | 'staff';
} | null;

export function NavBar() {
  const [user, setUser] = useState<User>(null);

  const handleLogin = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const username = formData.get('username') as string;
    const password = formData.get('password') as string;

    // This is a mock login. In a real app, you'd validate against a backend.
    if (username === 'teacher' && password === 'password') {
      setUser({ name: 'Teacher', role: 'staff' });
    } else if (username === 'student' && password === 'password') {
      setUser({ name: 'Student', role: 'student' });
    }
  };

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <header className="px-4 lg:px-6 h-16 flex items-center bg-blue-600">
      <Link className="flex items-center justify-center" href="/">
        <BookOpen className="h-6 w-6 text-white" />
        <span className="ml-2 text-2xl font-bold text-white">Project K</span>
      </Link>
      <nav className="ml-auto flex gap-4 sm:gap-6">
        <Link className="text-sm font-medium hover:underline text-white" href="/">
          Home
        </Link>
        <Link className="text-sm font-medium hover:underline text-white" href="/teachers">
          Our Teachers
        </Link>
        <Link className="text-sm font-medium hover:underline text-white" href="/courses">
          Our Courses
        </Link>
        <Link className="text-sm font-medium hover:underline text-white" href="/base">
          Our Base
        </Link>
        {user ? (
          <Button onClick={handleLogout} variant="ghost" className="text-white hover:text-gray-200">
            Logout
          </Button>
        ) : (
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" className="text-white hover:text-gray-200">Login</Button>
            </SheetTrigger>
            <SheetContent>
              <SheetHeader>
                <SheetTitle>Login to Project K</SheetTitle>
                <SheetDescription>
                  Enter your credentials to access your account.
                </SheetDescription>
              </SheetHeader>
              <form onSubmit={handleLogin} className="space-y-4 py-4">
                <div className="space-y-2">
                  <Label htmlFor="username">Username</Label>
                  <Input id="username" name="username" placeholder="Enter your username" />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input id="password" name="password" type="password" placeholder="Enter your password" />
                </div>
                <SheetFooter>
                  <SheetClose asChild>
                    <Button type="submit">Login</Button>
                  </SheetClose>
                </SheetFooter>
              </form>
            </SheetContent>
          </Sheet>
        )}
      </nav>
    </header>
  )
}

