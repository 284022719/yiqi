// netlify/functions/discord-status.js
const Discord = require('discord.js');

exports.handler = async (event, context) => {
  try {
    const client = new Discord.Client({
      intents: [Discord.Intents.FLAGS.GUILDS, Discord.Intents.FLAGS.GUILD_VOICE_STATES]
    });
    
    await client.login(process.env.DISCORD_BOT_TOKEN);
    
    const guild = await client.guilds.fetch('YOUR_DISCORD_GUILD_ID');
    await guild.channels.fetch();
    
    // 获取所有语音频道
    const voiceChannels = guild.channels.cache
      .filter(channel => channel.type === 'GUILD_VOICE')
      .sort((a, b) => a.position - b.position)
      .map(channel => {
        const members = Array.from(channel.members.values()).map(member => ({
          id: member.id,
          name: member.displayName,
          avatar: member.user.displayAvatarURL({ format: 'png', size: 128 }),
          isMuted: member.voice.mute || member.voice.selfMute,
          isDeafened: member.voice.deaf || member.voice.selfDeaf
        }));
        
        return {
          id: channel.id,
          name: channel.name,
          userLimit: channel.userLimit,
          members: members,
          memberCount: members.length
        };
      });
    
    client.destroy();
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        channels: voiceChannels,
        lastUpdated: new Date().toISOString()
      })
    };
  } catch (error) {
    console.error('Error fetching voice channels:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
