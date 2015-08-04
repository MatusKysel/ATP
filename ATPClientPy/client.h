#include <cstdlib>
#include <iostream>
#include <boost/bind.hpp>
#include <boost/asio.hpp>
#include <boost/asio/ssl.hpp>
#include <boost/system/error_code.hpp>

class ATPClient
{
public:
  ATPClient(boost::asio::io_service& io_service,
            boost::asio::ssl::context& context,
            boost::asio::ip::tcp::resolver::iterator endpoint_iterator);

  ~ATPClient() {}

  void handle_connect(const boost::system::error_code& error);

  void handle_handshake(const boost::system::error_code& error);

  void handle_write(const boost::system::error_code& error);

  void handle_read(const boost::system::error_code& error);

private:
  boost::asio::ssl::stream<boost::asio::ip::tcp::socket> socket_;
  boost::asio::streambuf request_;
  boost::asio::streambuf response_;
};
