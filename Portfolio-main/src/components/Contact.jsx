
import React, { useState } from "react";
import { motion } from "framer-motion";
import emailjs from "@emailjs/browser";

import { styles } from "../styles";
import { EarthCanvas } from "./canvas";
import { SectionWrapper } from "../hoc";
import { slideIn } from "../utils/motion";

const initialForm = {
  name: "",
  email: "",
  message: "",
};

const Contact = () => {
  const [form, setForm] = useState(initialForm);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({
    type: "",
    message: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (status.message) {
      setStatus({ type: "", message: "" });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (loading) return;

    // Read and clean environment variables
    const serviceId = (
      import.meta.env.VITE_APP_EMAILJS_SERVICE_ID || ""
    ).trim();

    const templateId = (
      import.meta.env.VITE_APP_EMAILJS_TEMPLATE_ID || ""
    ).trim();

    const publicKey = (
      import.meta.env.VITE_APP_EMAILJS_PUBLIC_KEY || ""
    ).trim();

    // Check configuration
    if (!serviceId || !templateId || !publicKey) {
      console.error("EmailJS configuration missing:", {
        serviceIdLoaded: !!serviceId,
        templateIdLoaded: !!templateId,
        publicKeyLoaded: !!publicKey,
      });

      setStatus({
        type: "error",
        message:
          "Email service configuration is missing. Please email me directly at amaanpatel0007@gmail.com.",
      });

      return;
    }

    // Safe diagnostics: never print the complete public key
    console.log("EMAILJS CONFIGURATION:", {
      serviceId,
      templateId,
      publicKeyLoaded: !!publicKey,
      publicKeyLength: publicKey.length,
      publicKeyStart: publicKey.slice(0, 3),
      publicKeyEnd: publicKey.slice(-3),
    });

    setLoading(true);
    setStatus({ type: "", message: "" });

    try {
      // Parameters matching your EmailJS template
      const templateParams = {
        from_name: form.name.trim(),
        from_email: form.email.trim(),
        reply_to: form.email.trim(),
        message: form.message.trim(),
      };

      console.log("Sending EmailJS request...");

      const response = await emailjs.send(
        serviceId,
        templateId,
        templateParams,
        {
          publicKey: publicKey,
        }
      );

      console.log("EmailJS SUCCESS:", {
        status: response.status,
        text: response.text,
      });

      setForm(initialForm);

      setStatus({
        type: "success",
        message:
          "Thank you! Your message has been sent successfully. I'll get back to you soon.",
      });

    } catch (error) {
      console.error("EMAILJS REQUEST FAILED:", {
        status: error?.status,
        text: error?.text,
        message: error?.message,
      });

      const errorMessage =
        error?.text ||
        error?.message ||
        "Unknown error";

      setStatus({
        type: "error",
        message:
          `Email failed: ${errorMessage}. Please email me directly at amaanpatel0007@gmail.com.`,
      });

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="xl:mt-12 flex xl:flex-row flex-col-reverse gap-10 overflow-hidden">

      {/* Contact Form */}
      <motion.div
        variants={slideIn("left", "tween", 0.2, 1)}
        className="flex-[0.75] bg-black-100 p-8 rounded-2xl"
      >
        <p className={styles.sectionSubText}>
          Get in touch
        </p>

        <h3 className={styles.sectionHeadText}>
          Contact.
        </h3>

        <form
          onSubmit={handleSubmit}
          className="mt-12 flex flex-col gap-8"
        >

          {/* Name */}
          <label className="flex flex-col">
            <span className="text-white font-medium mb-4">
              Your Name
            </span>

            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="What's your good name?"
              autoComplete="name"
              required
              maxLength={100}
              className="bg-tertiary py-4 px-6 placeholder:text-secondary text-white rounded-lg outline-none border-none font-medium"
            />
          </label>

          {/* Email */}
          <label className="flex flex-col">
            <span className="text-white font-medium mb-4">
              Your email
            </span>

            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="What's your email address?"
              autoComplete="email"
              required
              maxLength={254}
              className="bg-tertiary py-4 px-6 placeholder:text-secondary text-white rounded-lg outline-none border-none font-medium"
            />
          </label>

          {/* Message */}
          <label className="flex flex-col">
            <span className="text-white font-medium mb-4">
              Your Message
            </span>

            <textarea
              rows={7}
              name="message"
              value={form.message}
              onChange={handleChange}
              placeholder="What would you like to say?"
              required
              maxLength={5000}
              className="bg-tertiary py-4 px-6 placeholder:text-secondary text-white rounded-lg outline-none border-none font-medium"
            />
          </label>

          {/* Status */}
          {status.message && (
            <p
              role="status"
              aria-live="polite"
              className={
                status.type === "success"
                  ? "text-green-400"
                  : "text-red-400"
              }
            >
              {status.message}
            </p>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="bg-tertiary py-3 px-8 rounded-xl outline-none w-fit text-white font-bold shadow-md shadow-primary disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? "Sending..." : "Send"}
          </button>

        </form>
      </motion.div>

      {/* Earth Animation */}
      <motion.div
        variants={slideIn("right", "tween", 0.2, 1)}
        className="xl:flex-1 xl:h-auto md:h-[550px] h-[350px]"
      >
        <EarthCanvas />
      </motion.div>

    </div>
  );
};

export default SectionWrapper(Contact, "contact");
