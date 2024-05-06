#!/bin/bash

# While x < 10
x=1
while [[ $x -le 10 ]]
do
    # Read user input
    read -p "Pushup $x: Press enter to continue"
    # Increment x by 1 each time loops runs
    (( x ++ ))
done
echo "Kongrats! You did all your pushups!"

# Read from a file
read -r line; 
do
    echo "Line $x $line"
    (( x ++ ))
done < hamlet

# Until loop
until [[ $order == "coffee" ]]
    echo "Would you like coffee or tea?"
    read order
done
echo "\nExcellent choice! Here is your coffee."


#


