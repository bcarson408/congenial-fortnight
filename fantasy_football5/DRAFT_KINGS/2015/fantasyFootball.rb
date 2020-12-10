#!/Users/brcarson/.rvm/rubies/ruby-2.1.0/bin/ruby

require 'csv'
file='/Users/brcarson/FantasyFootball/QB_week1.csv'
customers = CSV.read('customers.csv')



f = File.open(file, "r")
f.each_line { |line|
  puts line
}

f.close