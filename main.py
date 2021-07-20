# -=-= Options =-=-
# All of these are required so make sure to do them

# -- Role IDs --
# IMPORTANT: MAKE SURE TO ADD THESE!
# ROLE_16 would be 16 credits etc
ROLE_16 = 0
ROLE_8 = 0
ROLE_4 = 0
ROLE_2 = 0
ROLE_1 = 0

# -- Bot Token --
# your bots token from discord.com/developers/applications
BOT_TOKEN = ""

# -- Items for Purchasing --
# add all of your items here with the price in the format of this:
# {"item_one" : 15, "item_two" : 10}
# MAKE SURE TO ADD COMMAS WHERE THEY ARE SUPPOSED TO GO!
# MAKE SURE THERE ARE NO CAPITAL LETTERS!
items = {"banana": 3, "apple": 1}

# -- Command Prefix --
# strings only, make sure to add "" or '' around them
COMMAND_PREFIX = "-"

# -- Custom Status --
# the status of the bot
# the bot will have "Playing" at the begining of it#
# if you know what your doing, you can mess around with it on line 35
STATUS = f"{COMMAND_PREFIX}help for help."

# imports
import discord # discord api
from discord import colour # colours omg
from discord.ext import commands # makes commands easier
import time # for the ping commmand

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all()) # bot var needed for discord.py
bot.remove_command("help") # remove old help command
shopping_carts = {} # define the empty shopping cart dictionary

@bot.event # when
async def on_ready(): # the bot is ready
    print(f"{bot.user.name} is ready.") # display in console
    await bot.change_presence(activity=discord.Game(name=STATUS), status=discord.Status.idle) # set status

@bot.command(aliases=["p"])
async def ping(ctx):
    time_before = time.time() # get unix time before sending message
    msg = await ctx.send("Pinging...") # send message and "await" for reply
    time_after = time.time() # record time after discord replies
    difference = int((time_after - time_before) * 1000) # equation for difference in time for milliseconds rounded
    embed = discord.Embed(title="Response Times", color=discord.Colour.blue()) # define embed stuff
    embed.add_field(name="API", value=f"`{difference}ms`")
    embed.add_field(name="Websocket", value=f"`{int(bot.latency * 1000)}ms`") # websocket ping is stored in the bot.latency var
    await msg.edit(embed=embed, content=f"{ctx.author.mention}") # edit the "Pinging..." msg to the embed

@bot.command(aliases=["h"])
async def help(ctx):
    des = f"""{COMMAND_PREFIX}additem (item) / adds item to cart
{COMMAND_PREFIX}removeitem (item) / remove item from cart
{COMMAND_PREFIX}cart [user] / view whats in someones cart
{COMMAND_PREFIX}credits [user] / view how much credits someone has
{COMMAND_PREFIX}checkout / go to the checkout
{COMMAND_PREFIX}stock / see what we have to sell
{COMMAND_PREFIX}help / shows this message""" # description text
    embed = discord.Embed(title="Help Command", description=des, colour=discord.Colour.blue()) # define embed stuff
    embed.set_footer(text="[] = optional / () = required")
    await ctx.send(embed=embed, content=ctx.author.mention) # send message

async def getCredits(member): # def getCredits function
    credits = 0 # set credits to 0 so we can add to it
    for role in member.roles: # for every role that the member has
        if ROLE_16 == role.id: # if the member has the 16 credits role
            credits += 16 # add 16 credits
        if ROLE_8 == role.id: # etc etc
            credits += 8
        if ROLE_4 == role.id:
            credits += 4
        if ROLE_2 == role.id:
            credits += 2
        if ROLE_1 == role.id:
            credits += 1
    return credits # return the amount of credits the member has

@bot.event # when
async def on_command_error(ctx, error): # theres an error in the command with no try statement
    if isinstance(error, commands.errors.MemberNotFound): # if the error is that the member that gave wasnt a member
        await ctx.send(f'{ctx.author.mention}, Not a valid user.') # let them know

@bot.command(aliases=["a"])
async def additem(ctx, *, item=None): # add item command
    global items # global declaration to be able to use/edit them
    global shopping_carts
    if item == None: # if they gave no item
       await ctx.send(f"{ctx.author.mention}, You need to state an item.") # say so
       return # stop command
    if item.lower() in items: # if the item said is in the items list
        if ctx.author.id not in shopping_carts: # if they dont have a basket already
            shopping_carts[ctx.author.id] = [item.lower()] # make one with a list which has the item in it
        else: # if they have a basket
            if item.lower() not in shopping_carts[ctx.author.id]: # if the item isnt in the basket
                shopping_carts[ctx.author.id].append(item.lower()) # add the item to the list
            else: # otherwise
                await ctx.send(f"{ctx.author.mention}, `{item}` is already in your cart.") # let them know
                return
        await ctx.send(f"{ctx.author.mention}, Added `{item}` to cart.") # if everything works, send this
    else:
        await ctx.send(f"{ctx.author.mention}, Couldn't find `{item}` in stock.") # if the item isnt in the items list, say they couldn't find the item

@bot.command(aliases=["r"])
async def removeitem(ctx, *, item=None): # remove item command
    global items # global declarations
    global shopping_carts
    if item == None: # this command is very similar to the add item command, only big difference is that
       await ctx.send(f"{ctx.author.mention}, You need to state an item.")
       return
    if item.lower() in items:
        if ctx.author.id not in shopping_carts:
            await ctx.send(f"{ctx.author.mention}, You don't have a cart.")
            return
        else:
            if item.lower() in shopping_carts[ctx.author.id]:
                shopping_carts[ctx.author.id].remove(item.lower()) # it removes the item (shocker)
            else:
                await ctx.send(f"{ctx.author.mention}, `{item}` isn't in your cart.")
                return
        await ctx.send(f"{ctx.author.mention}, Removed `{item}` to cart.")
    else:
        await ctx.send(f"{ctx.author.mention}, Couldn't find `{item}` in stock.")

@bot.command(aliases=["c"])
async def cart(ctx, *, user : discord.Member = None): # see whats in the cart
    if user == None: # if the member provided is none
        if ctx.author.id not in shopping_carts: # if the user who said the command doesnt have a cart
            await ctx.send(f"{ctx.author.mention}, You don't have a cart.") # state it
            return # stop command
        else: # otherwise
            total_cost = 0 # do variable stuff
            embed = discord.Embed(title=f"{ctx.author.name}'s Cart", color=discord.Color.blue())
            em_items = ""
            em_cost = ""
            for item in shopping_carts[ctx.author.id]: # for item in their cart
                em_items += f"`{item}`\n" # make fancy embed stuff
                em_cost += f"`{items[item]}`\n"
                total_cost += items[item]
            em_cost += f"{total_cost}"
            em_items += "Total:"
            embed.add_field(name="Items⠀⠀⠀⠀", value=em_items)
            embed.add_field(name="Cost", value=em_cost)
            await ctx.send(embed=embed, content=ctx.author.mention) # send the command
    else: # if they mentioned a user
        if user.id not in shopping_carts: # if they have a cart
            await ctx.send(f"{ctx.author.mention}, They don't have a cart.") # say so
            return
        else: # otherwise
            total_cost = 0 # variable stuff
            embed = discord.Embed(title=f"{user.name}'s Cart", color=discord.Color.blue())
            em_items = ""
            em_cost = ""
            for item in shopping_carts[user.id]: # embed stuff
                em_items += f"`{item}`\n"
                em_cost += f"`{items[item]}`\n"
                total_cost += items[item]
            em_cost += f"{total_cost}"
            em_items += "Total:"
            embed.add_field(name="Items⠀⠀⠀⠀", value=em_items)
            embed.add_field(name="Cost", value=em_cost)
            await ctx.send(embed=embed, content=ctx.author.mention) # send it

@bot.command(aliases=['balance', 'bal', "b"])
async def credits(ctx, *, user : discord.Member = None): # states amount of credits a user has
    if user == None: # if they didnt state a user
        # use the getCredits function to get the credits and send it
        embed = discord.Embed(title=f"{ctx.author.name}'s Credits", description=f"{ctx.author.name} has {await getCredits(ctx.author)} credits.", colour=discord.Colour.blue())
        await ctx.send(embed=embed, content=ctx.author.mention)
    else: # if they stated a user
        # use the getCredits function to get the credits and send it
        embed = discord.Embed(title=f"{user.name}'s Credits", description=f"{user.name} has {await getCredits(user)} credits.", colour=discord.Colour.blue())
        await ctx.send(embed=embed, content=ctx.author.mention)

@bot.command()
async def checkout(ctx):
    if ctx.author.id not in shopping_carts: # if user doesnt have a cart
        await ctx.send(f"{ctx.author.mention}, You don't have a cart.") # alert them
        return
    credits = await getCredits(ctx.author) # get the amount of credits the user has
    total_cost = 0
    em_items = "" # test vars to 0 / empty so i can add to them
    em_cost = ""
    for item in shopping_carts[ctx.author.id]: # for every item in the users cart
        em_items += f"`{item}`\n" # add the item to the embed list
        em_cost += f"`{items[item]}`\n" # add the cost
        total_cost += items[item] # add the cost to the total cost
    em_cost += f"{total_cost}" # makes embed look neat and formated
    em_items += "Total:"
    embed = discord.Embed(title=f"{ctx.author.name}'s Cart", color=discord.Color.blue(), description=f"You have {credits} credits, you will have {credits - total_cost} left after. Are you sure you want to purchase these items?")
    embed.add_field(name="Items⠀⠀⠀⠀", value=em_items) # set embed values
    embed.add_field(name="Cost", value=em_cost)
    embed.set_footer(text="Reply with `yes` or `no`. Reply within 10 seconds.")
    if total_cost <= credits: # if they have enough credits
        def wait_for_reply(message): # define a function to check messages sent
            return message.channel == ctx.channel and message.author == ctx.author # returns True if the channel is the same as the one where the original cmd was sent
        await ctx.send(embed=embed, content=ctx.author.mention) # send the embed we defined earlier
        try: # try to 
            reply = await bot.wait_for("message", check=wait_for_reply, timeout=10) # wait for message with the check as "wait_for_reply"
        except: # if its gone longer than 10 seconds
            await ctx.send("Timeout, retry.") # timeout msg is sent
        else: # if not and there is a message
            if reply.content.lower() == "yes": # if the message sent (in its lowercase format) is equal to "yes"
                credits_left = credits - total_cost # find out how many credits the user will have left
                role16 = ctx.guild.get_role(ROLE_16) # role ids for all of the amounts
                role8 = ctx.guild.get_role(ROLE_8)
                role4 = ctx.guild.get_role(ROLE_4)
                role2 = ctx.guild.get_role(ROLE_2)
                role1 = ctx.guild.get_role(ROLE_1)
                await ctx.author.remove_roles(role1) # remove all of their credit roles if they have them
                await ctx.author.remove_roles(role2)
                await ctx.author.remove_roles(role4)
                await ctx.author.remove_roles(role8)
                await ctx.author.remove_roles(role16)
                if credits_left > 0: # if they have more than 0 credits left (1 or more)
                    if credits_left >= 16: # if credits left is more or equal to 16
                        await ctx.author.add_roles(role16) # give 16 credit role
                        credits_left -= 16 # remove 16 credits from the remaining needed to return
                    if credits_left >= 8: # etc
                        await ctx.author.add_roles(role8)
                        credits_left -= 8
                    if credits_left >= 4:
                        await ctx.author.add_roles(role4)
                        credits_left -= 4
                    if credits_left >= 2:
                        await ctx.author.add_roles(role2)
                        credits_left -= 2
                    if credits_left >= 1:
                        await ctx.author.add_roles(role1)
                        credits_left -= 1
                
                # now here, you do whatever you want to after they have purchased the items.
                # shopping_carts[ctx.author.id] is the list with all of the items in it
                # use that to make if statements to do certain things like make api calls or whatever
                # youre smart, you will probably know what to do here 
            
            else: # if the reply doesnt equla "yes"
                await ctx.send("Ok, I canceled.") # say it canceled
    else: # if they dont have enough credits
        total_cost = 0 # do all of the embed stuff that we did again, except saying they dont have enough credits
        em_items = ""
        em_cost = ""
        for item in shopping_carts[ctx.author.id]:
            em_items += f"`{item}`\n"
            em_cost += f"`{items[item]}`\n"
            total_cost += items[item]
        em_cost += f"{total_cost}"
        em_items += "Total:"
        embed = discord.Embed(title=f"{ctx.author.name}'s Cart", color=discord.Color.red(), description=f"You don't have enough credits for this purchase.\nYou have {credits} credits, you need {total_cost - credits} more credits.")
        embed.add_field(name="Items⠀⠀⠀⠀", value=em_items)
        embed.add_field(name="Cost", value=em_cost)
        await ctx.send(content=ctx.author.mention, embed=embed) # and send it to the user

@bot.command(aliases=['shop', "s"])
async def stock(ctx): # simple command which sends the items in the items dictionary
    z = ""
    for x, y in items.items(): # for every item in the items dictionary
        z += f"Item: {x} / Cost: {y}\n" # x = name y = price
    embed=discord.Embed(title="Items in Shop", description=z, colour=discord.Colour.blue())
    await ctx.send(embed=embed, content=ctx.author.mention) # send

bot.run(BOT_TOKEN) # run bot