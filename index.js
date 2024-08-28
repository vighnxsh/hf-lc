import fetch from 'node-fetch';
import fs from 'fs/promises';

async function query(data) {
    const response = await fetch(
        "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
        {
            headers: {
                Authorization: "Bearer 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",
                "Content-Type": "application/json",
            },
            method: "POST",
            body: JSON.stringify(data),
        }
    );

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        const result = await response.json();
        if (result.error) {
            throw new Error(result.error);
        }
    }

    return response.buffer();
}

function saveImage(buffer) {
    const fileName = 'generated_image.png';
    fs.writeFile(fileName, buffer, (err) => {
        if (err) {
            console.error("Error saving image:", err);
        } else {
            console.log(`Image saved as ${fileName}`);
        }
    });
}

async function retryQuery(data, maxRetries = 5, delay = 10000) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            const response = await query(data);
            console.log("Image generated successfully");
            saveImage(response);
            return;
        } catch (error) {
            console.log(`Attempt ${i + 1} failed: ${error.message}`);
            if (error.message.includes("currently loading")) {
                console.log(`Retrying in ${delay / 1000} seconds...`);
                await new Promise(resolve => setTimeout(resolve, delay));
            } else {
                throw error; // If it's not a loading error, rethrow it
            }
        }
    }
    throw new Error("Max retries reached. The model is still loading.");
}

retryQuery({"inputs": "Spiderman vs naruto  in anime style"}).catch((error) => {
    console.error("Error generating image:", error.message);
});

