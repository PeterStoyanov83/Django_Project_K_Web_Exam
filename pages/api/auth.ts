import type { NextApiRequest, NextApiResponse } from 'next'

type User = {
  id: number;
  name: string;
  role: 'student' | 'staff';
}

type AuthResponse = {
  user?: User;
  error?: string;
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<AuthResponse>
) {
  if (req.method === 'POST') {
    const { username, password } = req.body;

    // This is a mock authentication. In a real app, you'd validate against a database.
    if (username === 'teacher' && password === 'password') {
      res.status(200).json({ user: { id: 1, name: 'Teacher', role: 'staff' } });
    } else if (username === 'student' && password === 'password') {
      res.status(200).json({ user: { id: 2, name: 'Student', role: 'student' } });
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}

