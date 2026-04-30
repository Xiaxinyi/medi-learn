export interface User {
  id: string;
  phone?: string;
  nickname?: string;
  realName?: string;
  avatarUrl?: string;
  email?: string;
  gender?: 'male' | 'female' | 'other';
  birthday?: string;
  bio?: string;
  role: 'admin' | 'user';
  level: number;
  experience: number;
  levelName?: string;
  levelColor?: string;
  nextLevelExp?: number;
  levelProgress: number;
  totalScore: number;
  streakDays: number;
}

export interface AttributeTag {
  id: string;
  name: string;
  groupName?: string;
  color?: string;
}

export interface HerbImage {
  id: string;
  image_url: string;
  thumbnail_url?: string;
  sort_order: number;
  is_cover: number;
  created_at?: number;
}

export interface Herb {
  id: string;
  name: string;
  latinName?: string;
  aliases?: string[];
  attributes: AttributeTag[];
  efficacy: string;
  indications: string;
  dosage: string;
  contraindications?: string;
  images: HerbImage[];
  category: string;
  origin?: string;
  isFavorite: boolean;
  notes: Note[];
  createdAt: number;
}

export interface Note {
  id: string;
  content: string;
  createdAt: number;
}

export interface Question {
  id: string;
  type: 'single' | 'multiple';
  content: string;
  options: Option[];
  correctAnswers: string[];
  explanation: string;
  difficulty: 'easy' | 'medium' | 'hard';
  tags: string[];
  herbIds?: string[];
}

export interface Option {
  id: string;
  option_key: string;
  content: string;
}

export interface Formula {
  id: string;
  name: string;
  source?: string;
  category: string;
  indications: string;
  usage?: string;
  modifications?: string;
  precautions?: string;
  herbs: FormulaHerbItem[];
}

export interface FormulaHerbItem {
  herbId: string;
  herbName: string;
  dosage?: string;
  role: 'chief' | 'deputy' | 'assistant' | 'envoy';
}

export interface AnswerRecord {
  id: string;
  questionId: string;
  userAnswers: string[];
  isCorrect: boolean;
  score: number;
  timeSpent: number;
  answeredAt: number;
}

export interface ExamResult {
  id: string;
  examName: string;
  totalQuestions: number;
  correctCount: number;
  score: number;
  maxScore: number;
  timeSpent: number;
  completedAt: number;
}

export interface WrongAnswer {
  id: string;
  questionId: string;
  userAnswers: string[];
  correctAnswers: string[];
  wrongCount: number;
  lastWrongAt: number;
  isMastered: boolean;
}

export interface Feedback {
  id: string;
  userId: string;
  type: 'suggestion' | 'bug' | 'complaint' | 'other';
  title: string;
  content: string;
  contact?: string;
  images?: string[];
  status: 'pending' | 'processing' | 'resolved' | 'rejected';
  adminReply?: string;
  repliedAt?: number;
}

export interface LevelConfig {
  level: number;
  name: string;
  icon?: string;
  minExperience: number;
  maxExperience: number;
  color: string;
  privileges: string[];
}

export interface ExperienceLog {
  id: string;
  userId: string;
  type: string;
  description: string;
  experience: number;
  balance: number;
  relatedId?: string;
  createdAt: number;
}

export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

export interface PageResult<T = any> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
}
