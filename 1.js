const express = require('express');
const { Client, middleware } = require('@line/bot-sdk');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 3000;

const config = {
    channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN,
    channelSecret: process.env.CHANNEL_SECRET
};

const client = new Client(config);

app.use(middleware(config));
app.use(bodyParser.json());

app.post('/webhook', (req, res) => {
    Promise.all(req.body.events.map(handleEvent))
        .then((result) => res.json(result))
        .catch((err) => {
            console.error(err);
            res.status(500).end();
        });
});

function handleEvent(event) {
    // 檢查事件類型是否為訊息
    if (event.type !== 'message' || event.message.type !== 'text') {
        return Promise.resolve(null);
    }

    // 紀錄事件來源信息
    const source = event.source;
    const logData = `User ID: ${source.userId}, Group ID: ${source.groupId}, Room ID: ${source.roomId}\n`;

    // 將來源信息寫入檔案或顯示在控制台
    fs.appendFileSync('group_ids.log', logData);
    console.log(logData);

    // 簡單回應收到的訊息
    return client.replyMessage(event.replyToken, {
        type: 'text',
        text: `收到訊息：${event.message.text}`
    });
}

app.listen(port, () => {
    console.log(`Server running on ${port}`);
});
