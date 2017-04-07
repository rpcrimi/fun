require 'json'
require 'optparse'
require 'net/http'

class AnagramClient
  def initialize(args=[])
    options = parse_opts(args)

    @dictionary = options[:dictionary] || 'dictionary.txt'
    @host = options[:host] || '192.168.99.100'
    @port = options[:port] || '3000'
  end

  def build_uri(path, query=nil)
    URI::HTTP.new('http', nil, @host, @port, nil, path, nil, query, nil)
  end

  def post(path, query=nil, body=nil)
    uri = build_uri(path, query)
    req = Net::HTTP::Post.new(uri.request_uri, initheader = {'Content-Type' =>'application/json'})
    if body
      req.body = body.to_json
    else
      file = File.open(@dictionary, "r")
      words = file.read.split()
      file.close
      req.body = {'words' => words}.to_json
    end
    http = Net::HTTP.new(uri.host, uri.port)
    res = http.request(req)
  end

  def get(path, query=nil)
    Net::HTTP.get_response(build_uri(path, query))
  end

  def delete(path)
    uri = build_uri(path)
    req = Net::HTTP::Delete.new(uri.request_uri, initheader = {'Content-Type' =>'application/json'})
    http = Net::HTTP.new(uri.host, uri.port)
    res = http.request(req)
  end

  private

  def parse_opts(args)
    options = {}

    OptionParser.new do |opts|
      opts.banner = "Usage: ruby anagram_test.rb -- [options]"

      opts.on("-n", "--hostname HOSTNAME", "defaults to localhost") do |h|
        options[:host] = h
      end

      opts.on("-p", "--port PORT_NUMBER", "defaults to 3000") do |p|
        options[:port] = p
      end

      opts.on_tail("-h", "--help", "Show help message") do
        puts opts
        exit
      end
    end.parse!(args)

    options
  end
end