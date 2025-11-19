# Website Deployment Guide

This guide provides step-by-step instructions for deploying the portfolio website to three popular platforms: Vercel, Netlify, and GitHub Pages. All three platforms offer a free tier that is perfect for hosting a personal portfolio website.

## Before You Begin

Before you deploy the website, make sure you have:

1.  **A GitHub account:** If you don't have one, you can sign up for free at [https://github.com](https://github.com).
2.  **Pushed your code to a GitHub repository:** Create a new repository on GitHub and push the `portfolio-website` directory to it.
3.  **Replaced the placeholder links:** In the `portfolio-website` code, replace all instances of `https://github.com/your-username/your-repo` with the actual URL of your GitHub repository.

## Option 1: Deploying to Vercel (Recommended)

Vercel is the company behind Next.js, so it's the easiest and most optimized platform for deploying Next.js websites.

1.  **Sign up for Vercel:** Go to [https://vercel.com](https://vercel.com) and sign up for a free account using your GitHub account.
2.  **Import your project:** Once you're logged in, you'll be taken to your dashboard. Click the "Add New..." button and select "Project".
3.  **Connect to your Git repository:** Vercel will ask you to connect to your Git provider. Choose "GitHub" and authorize Vercel to access your repositories.
4.  **Select your repository:** You'll see a list of your GitHub repositories. Find the repository for your `portfolio-website` and click the "Import" button.
5.  **Configure your project:** Vercel will automatically detect that you're deploying a Next.js project and will pre-configure the build settings for you. You don't need to change anything here.
6.  **Deploy:** Click the "Deploy" button. Vercel will now build and deploy your website. This may take a few minutes.
7.  **Done!** Once the deployment is complete, you'll be given a URL where you can view your live website.

## Option 2: Deploying to Netlify

Netlify is another popular platform for deploying modern web applications.

1.  **Sign up for Netlify:** Go to [https://www.netlify.com](https://www.netlify.com) and sign up for a free account using your GitHub account.
2.  **Create a new site:** From your Netlify dashboard, click the "Add new site" button and choose "Import an existing project".
3.  **Connect to your Git provider:** Choose "GitHub" and authorize Netlify to access your repositories.
4.  **Select your repository:** You'll see a list of your GitHub repositories. Find the repository for your `portfolio-website` and select it.
5.  **Configure your build settings:** Netlify will automatically detect that you're deploying a Next.js project and will pre-configure the build settings for you. You don't need to change anything here.
6.  **Deploy:** Click the "Deploy site" button. Netlify will now build and deploy your website. This may take a few minutes.
7.  **Done!** Once the deployment is complete, you'll be given a URL where you can view your live website.

## Option 3: Deploying to GitHub Pages

GitHub Pages is a free hosting service provided by GitHub. While it's a great option for static websites, it's not as straightforward to deploy a Next.js application to GitHub Pages as it is to Vercel or Netlify.

1.  **Install `gh-pages`:** You'll need to install the `gh-pages` package as a dev dependency. Open a terminal, navigate to your `portfolio-website` directory, and run the following command:
    ```bash
    npm install --save-dev gh-pages
    ```
2.  **Update `package.json`:** Open your `package.json` file and add the following scripts:
    ```json
    "scripts": {
      "predeploy": "npm run build",
      "deploy": "gh-pages -d out"
    }
    ```
3.  **Configure `next.config.js`:** You'll need to configure the `basePath` in your `next.config.js` file to match your repository name. For example, if your repository name is `my-portfolio`, your `next.config.js` file should look like this:
    ```javascript
    /** @type {import('next').NextConfig} */
    const nextConfig = {
      basePath: '/my-portfolio',
      output: 'export',
    };

    module.exports = nextConfig;
    ```
4.  **Deploy:** Now, you can deploy your website by running the following command in your terminal:
    ```bash
    npm run deploy
    ```
    This command will build your website and push the `out` directory to a new `gh-pages` branch in your repository.
5.  **Configure your repository:** In your GitHub repository, go to the "Settings" tab and then to the "Pages" section. Under "Source", select the `gh-pages` branch and the `/ (root)` directory.
6.  **Done!** It may take a few minutes for your website to go live. Once it does, you'll be able to view it at `https://your-username.github.io/your-repo`.
