
import {
  logo,
  backend,
  creator,
  mobile,
  web,
  github,
  menu,
  close,
  css,
  gearXpert,
  project2,
  project3,
  mysql,
  express,
  aws,
  mui,
  gsap,
  framer,
  figma,
  git,
  html,
  javascript,
  mongodb,
  nodejs,
  reactjs,
  redux,
  tailwind,
  threejs,
  firstTestimonial,
  secondTestimonial,
  thirdTestimonial,
} from "../assets";

// Company image
import tekisky from "../assets/company/tekisky.png";

// Project images
import testcase from "../assets/testcase1.png";
import taskflow from "../assets/taskflow.png";
import fraudguard from "../assets/fraudguard.png";
import concordRepo from "../assets/concord.png";

// Technology images
import sass from "../assets/tech/sass.png";
import python from "../assets/tech/python.png";
import java from "../assets/tech/java.png";
import postman from "../assets/tech/postman.png";

// Navigation
export const navLinks = [
  {
    id: "about",
    title: "About",
  },
  {
    id: "projects",
    title: "Projects",
  },
  {
    id: "contact",
    title: "Contact",
  },
];

// Services
const services = [
  {
    title: "Full-Stack Developer",
    icon: web,
  },
  {
    title: "Frontend Developer",
    icon: mobile,
  },
  {
    title: "Backend Developer",
    icon: backend,
  },
  {
    title: "Artificial Intelligence and Machine learning",
    icon: creator,
  },
];

// Technologies
const technologies = [
  {
    name: "HTML 5",
    icon: html,
  },
  {
    name: "CSS 3",
    icon: css,
  },
  {
    name: "JavaScript",
    icon: javascript,
  },
  {
    name: "React JS",
    icon: reactjs,
  },
  {
    name: "Tailwind CSS",
    icon: tailwind,
  },
  {
    name: "Node JS",
    icon: nodejs,
  },
  {
    name: "Express Js",
    icon: express,
  },
  {
    name: "MongoDB",
    icon: mongodb,
  },
  {
    name: "MySql",
    icon: mysql,
  },
  {
    name: "Sass",
    icon: sass,
  },
  {
    name: "Python",
    icon: python,
  },
  {
    name: "Git",
    icon: git,
  },
  {
    name: "Java",
    icon: java,
  },
  {
    name: "Postman",
    icon: postman,
  },
];

// Experience
const experiences = [
  {
    title: "Full-Stack Developer",
    company_name: "Tekisky",
    icon: tekisky,
    iconBg: "#383E56",
    date: "Jan 2023 - present",
    points: [
      "Developing and maintaining web applications using MERN technologies.",
      "Collaborating with cross-functional teams including designers, product managers, and other developers to create high-quality products.",
      "Implementing responsive design and ensuring cross-browser compatibility.",
      "Participating in code reviews and providing constructive feedback to other developers.",
    ],
  },
];

// Testimonials
const testimonials = [
  {
    testimonial:
      "I thought it was impossible to make a website as beautiful as our product, but Huzaif proved me wrong.",
    name: "MD Mustaqeem",
    designation: "Ecommerce",
    company: "QuickMart",
    image: firstTestimonial,
  },
  {
    testimonial:
      "I've never met a web developer who truly cares about their clients' success like Huzaif does.",
    name: "Abdul Raheman",
    designation: "Ecommerce Business",
    company: "justbuyz",
    image: secondTestimonial,
  },
  {
    testimonial:
      "After Huzaif optimized our website, our traffic increased by 50%. We can't thank them enough!",
    name: "James Wang",
    designation: "CTO",
    company: "456 Enterprises",
    image: thirdTestimonial,
  },
];

// Projects
const projects = [
  {
    name: "AI TestGen – AI-Driven Test Case Generator",
    description:
      "Built a full-stack application using React.js, Node.js, and Gemini AI to automate test case generation. Integrated GitHub OAuth to analyze user repositories and generate multi-language test suites.",
    tags: [
      { name: "React.js", color: "blue-text-gradient" },
      { name: "Node.js", color: "white-text-gradient" },
      { name: "Gemini AI", color: "pink-text-gradient" },
      { name: "GitHub API", color: "green-text-gradient" },
      { name: "OAuth 2.0", color: "blue-text-gradient" },
    ],
    image: testcase,
    source_code_link:
      "https://github.com/AmanPatel470/AI-Testcase-Generator",
  },
  {
    name: "FraudGuard – Fake Job Detection Using ML",
    description:
      "Built a Flask API serving a Logistic Regression model trained with TF-IDF to detect fake job postings, achieving 90% accuracy on test data. Integrated the API with a Node.js backend and React frontend.",
    tags: [
      { name: "Python", color: "blue-text-gradient" },
      { name: "Flask", color: "white-text-gradient" },
      { name: "Node.js", color: "pink-text-gradient" },
      { name: "TF-IDF", color: "green-text-gradient" },
      { name: "Logistic Regression", color: "blue-text-gradient" },
    ],
    image: fraudguard,
    source_code_link:
      "https://github.com/AmanPatel470/FraudGuard",
  },
  {
    name: "Concord MCP – Open Source Contribution",
    description:
      "Implemented duplicate message delivery protection in the agent relay using SHA-256 fingerprints and an in-memory cache. Improved cache capacity management, preserved pending deliveries, reused in-flight requests, and added regression tests for filesystem portability and workspace isolation.",
    tags: [
      { name: "TypeScript", color: "blue-text-gradient" },
      { name: "Node.js", color: "white-text-gradient" },
      { name: "SHA-256", color: "pink-text-gradient" },
      { name: "Vitest", color: "green-text-gradient" },
      { name: "Open Source", color: "blue-text-gradient" },
    ],
    image: concordRepo,
    source_code_link:
      "https://github.com/Get-Concord-AI/concord-mcp",
  },
];

export {
  services,
  technologies,
  experiences,
  testimonials,
  projects,
};
