import type { NextApiRequest, NextApiResponse } from 'next'

type Course = {
  id: number;
  name: string;
  description: string;
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Course[]>
) {
  if (req.method === 'GET') {
    // This is mock data. In a real app, you'd fetch this from a database.
    const courses: Course[] = [
      { id: 1, name: 'Web Development Basics', description: 'Learn the fundamentals of web development.' },
      { id: 2, name: 'Advanced JavaScript', description: 'Master advanced JavaScript concepts and techniques.' },
      { id: 3, name: 'Data Science with Python', description: 'Explore data science using Python and popular libraries.' },
    ];
    res.status(200).json(courses);
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}

