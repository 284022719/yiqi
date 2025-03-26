// netlify/functions/member-status.js
const Discord = require('discord.js');

exports.handler = async (event, context) => {
  try {
    const client = new Discord.Client({
      intents: [Discord.Intents.FLAGS.GUILD_PRESENCES, Discord.Intents.FLAGS.GUILD_MEMBERS]
    });
    
    await client.login(process.env.DISCORD_BOT_TOKEN);
    
    const guild = await client.guilds.fetch('YOUR_DISCORD_GUILD_ID');
    await guild.members.fetch();
    
    const members = guild.members.cache.map(member => {
      let status = 'offline';
      let activity = '';
      
      if (member.presence) {
        status = member.presence.status;
        
        if (member.presence.activities.length > 0) {
          const gameActivity = member.presence.activities.find(a => a.type === 'PLAYING');
          if (gameActivity) {
            activity = gameActivity.name;
            
            // 判断活动类型
            if (gameActivity.name.includes('魔兽世界')) {
              if (gameActivity.details) {
                if (gameActivity.details.includes('团队')) {
                  status = 'raid';
                } else if (gameActivity.details.includes('地下城')) {
                  status = 'dungeon';
                }
              }
            }
          }
        }
      }
      
      return {
        id: member.id,
        name: member.displayName,
        avatar: member.user.displayAvatarURL({ format: 'png', size: 128 }),
        status,
        activity,
        roles: member.roles.cache.map(role => role.name)
      };
    });
    
    client.destroy();
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        members,
        lastUpdated: new Date().toISOString()
      })
    };
  } catch (error) {
    console.error('Error fetching member status:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
