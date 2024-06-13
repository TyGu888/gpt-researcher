import discord
import nest_asyncio
from gpt_researcher import GPTResearcher
import asyncio
import os

nest_asyncio.apply()

TOKEN = ''
# Define the intents

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True  # Ensure this is enabled for reading message content

client = discord.Client(intents=intents)

# Default instructions for the GPT researcher
DEFAULT_INSTRUCTIONS = "You are an AI assistant that provides detailed research reports."

async def get_report(query: str, report_type: str, instructions: str = DEFAULT_INSTRUCTIONS) -> str:
    researcher = GPTResearcher(query, report_type, instructions)
    research_result = await researcher.conduct_research()
    report = await researcher.write_report()
    return report

def split_message(message, max_length=2000):
    # Split the message into chunks of max_length
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

@client.event
async def on_message(message):
    print(f"Received a message: {message.content} in {message.channel} (Guild: {message.guild})")
    print(client.user.id)

    if message.author == client.user:
        print("Ignoring message from self.")
        return

    if isinstance(message.channel, discord.DMChannel):
        print("Message is in DM.")
    else:
        print("Message is in a server channel.")

    # Manually check if the message mentions the bot by checking for the bot's ID in the content
    if f'<@!{client.user.id}>' in message.content or f'<@{client.user.id}>' in message.content or message.content.startswith('!research'):
        print(f"Bot was mentioned in {message.channel}: {message.content}")
        query = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()
        report_type = "research_report"
        if query:
            try:
                report = await get_report(query, report_type)
                messages = split_message(report)
                for msg in messages:
                    await message.channel.send(msg)
                print("Report sent.")
            except Exception as e:
                await message.channel.send(f"An error occurred: {e}")
                print(f"Error occurred: {e}")
        else:
            await message.channel.send("Please provide a query for the research report.")
            print("Query not provided.")
    else:
        print("Bot was not mentioned in the message.")

if __name__ == "__main__":
    client.run(TOKEN)