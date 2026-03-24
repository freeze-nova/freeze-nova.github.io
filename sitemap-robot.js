const fs = require("fs");
const path = require("path");

// Đường dẫn tới file sitemap.xml và robots.txt
const sitemapPath = path.join(__dirname, "sitemap.xml");
const robotsPath = path.join(__dirname, "robots.txt");

// Hàm để cập nhật sitemap.xml
function updateSitemap() {
  fs.readFile(sitemapPath, "utf8", (err, data) => {
    if (err) {
      console.error(`Không thể đọc file sitemap: ${sitemapPath}`, err);
      return;
    }

    // Cập nhật thẻ <lastmod> với ngày hiện tại
    const updatedData = data.replace(
      /<lastmod>.*?<\/lastmod>/g,
      `<lastmod>${new Date().toISOString()}</lastmod>`
    );

    fs.writeFile(sitemapPath, updatedData, "utf8", (err) => {
      if (err) {
        console.error(`Không thể ghi file sitemap: ${sitemapPath}`, err);
      } else {
        console.log(`Đã cập nhật sitemap: ${sitemapPath}`);
      }
    });
  });
}

// Nội dung mẫu cho robots.txt
const robotsContent = `
User-agent: *
Disallow: /private/
Allow: /

Sitemap: https://freeze-nova.github.io/sitemap.xml
`;

// Hàm để cập nhật robots.txt
function updateRobots() {
  fs.writeFile(robotsPath, robotsContent, "utf8", (err) => {
    if (err) {
      console.error(`Không thể ghi file robots.txt: ${robotsPath}`, err);
    } else {
      console.log(`Đã cập nhật robots.txt: ${robotsPath}`);
    }
  });
}

// Gọi các hàm cập nhật
updateSitemap();
updateRobots();
