
import React, { useEffect, useRef } from "react";
import { Tilt } from "react-tilt";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

import { styles } from "../styles";
import { github } from "../assets";
import { SectionWrapper } from "../hoc";
import { projects } from "../constants";

gsap.registerPlugin(ScrollTrigger);

const ProjectCard = ({
  name,
  description,
  tags,
  image,
  source_code_link,
}) => {
  const cardRef = useRef(null);

  useEffect(() => {
    const el = cardRef.current;

    const animation = gsap.fromTo(
      el,
      {
        opacity: 0,
        y: 100,
      },
      {
        opacity: 1,
        y: 0,
        scrollTrigger: {
          trigger: el,
          start: "top bottom",
          end: "top center",
          scrub: true,
          markers: false,
        },
      }
    );

    return () => {
      animation.scrollTrigger?.kill();
      animation.kill();
    };
  }, []);

  return (
    <div ref={cardRef} className="h-full w-full">
      <Tilt
        options={{
          max: 45,
          scale: 1,
          speed: 450,
        }}
        className="bg-tertiary p-5 rounded-2xl sm:w-[360px] w-full h-full flex flex-col"
      >
        {/* Project Image */}
        <div className="relative w-full h-[230px] flex-shrink-0">
          <img
            src={image}
            alt={`${name} project preview`}
            className="w-full h-full object-cover object-center rounded-2xl"
          />

          {/* GitHub Button */}
          <div className="absolute inset-0 flex justify-end m-3 card-img_hover">
            <a
              href={source_code_link}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={`View ${name} source code on GitHub`}
              className="black-gradient w-10 h-10 rounded-full flex justify-center items-center cursor-pointer"
            >
              <img
                src={github}
                alt=""
                className="w-1/2 h-1/2 object-contain"
              />
            </a>
          </div>
        </div>

        {/* Project Information */}
        <div className="mt-5 flex-1">
          <h3 className="text-white font-bold text-[24px] leading-8">
            {name}
          </h3>

          <p className="mt-3 text-secondary text-[14px] leading-6">
            {description}
          </p>
        </div>

        {/* Technology Tags */}
        <div className="mt-4 flex flex-wrap gap-2">
          {tags.map((tag) => (
            <p
              key={`${name}-${tag.name}`}
              className={`text-[14px] ${tag.color}`}
            >
              #{tag.name}
            </p>
          ))}
        </div>
      </Tilt>
    </div>
  );
};

const Works = () => {
  useEffect(() => {
    const animation = gsap.fromTo(
      ".project-card",
      {
        opacity: 0,
        y: 100,
      },
      {
        opacity: 1,
        y: 0,
        stagger: 0.1,
        scrollTrigger: {
          trigger: ".works-container",
          start: "top bottom",
          end: "top center",
          scrub: true,
          markers: false,
        },
      }
    );

    return () => {
      animation.scrollTrigger?.kill();
      animation.kill();
    };
  }, []);

  return (
    <>
      <div>
        <p className={styles.sectionSubText}>My work</p>
        <h2 className={styles.sectionHeadText}>Projects.</h2>
      </div>

      <div className="w-full flex">
        <p className="mt-3 text-secondary text-[17px] max-w-3xl leading-[30px]">
          Following projects showcase my skills and experience through
          real-world examples of my work. Each project is briefly described
          with links to code repositories and live demos. It reflects my
          ability to solve complex problems, work with different technologies,
          and manage projects effectively.
        </p>
      </div>

      {/* Responsive Project Grid */}
      <div className="works-container mt-20 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 items-stretch justify-items-center gap-5">
        {projects.map((project, index) => (
          <div
            key={`project-${index}`}
            className="project-card h-full w-full flex justify-center"
          >
            <ProjectCard {...project} />
          </div>
        ))}
      </div>
    </>
  );
};

export default SectionWrapper(Works, "projects");
