#include "client.h"


ATPClient::ATPClient(boost::asio::io_service& io_service,
                     boost::asio::ssl::context& context,
                     boost::asio::ip::tcp::resolver::iterator endpoint_iterator)
  : socket_(io_service, context)
{
  socket_.set_verify_mode(boost::asio::ssl::verify_none);


  boost::asio::async_connect(socket_.lowest_layer(), endpoint_iterator,
                             boost::bind(&ATPClient::handle_connect, this,
                                         boost::asio::placeholders::error));
}

void ATPClient::handle_connect(const boost::system::error_code& error)
{
  if (!error)
  {
    socket_.async_handshake(boost::asio::ssl::stream_base::client,
                            boost::bind(&ATPClient::handle_handshake, this,
                                        boost::asio::placeholders::error));
  }
  else
  {
    std::cout << "Connect failed: " << error.message() << "\n";
  }
}

void ATPClient::handle_handshake(const boost::system::error_code& error)
{
  if (!error)
  {
    std::ostream request_stream(&request_);
    request_stream << "ATP/0.1\n";
    request_stream << "TALK TO THE HAND\n";
    request_stream << "I NEED YOUR CLOTHES YOUR BOOTS AND YOUR MOTORCYCLE\n";
    request_stream << "YOU HAVE BEEN TERMINATED\n";
    request_stream << "\r\n";

    boost::asio::async_write(socket_,
                             request_,
                             boost::bind(&ATPClient::handle_write, this,
                                         boost::asio::placeholders::error));
  }
  else
  {
    std::cout << "Handshake failed: " << error.message() << "\n";
  }
}

void ATPClient::handle_write(const boost::system::error_code& error)
{
  if (!error)
  {
    boost::asio::async_read_until(socket_, response_, "\r\n",
                                  boost::bind(&ATPClient::handle_read, this,
                                              boost::asio::placeholders::error));
  }
  else
  {
    std::cout << "Write failed: " << error.message() << "\n";
  }
}

void ATPClient::handle_read(const boost::system::error_code& error)
{
  if (!error)
  {

    std::istream response_stream(&response_);
    std::string atp_version;
    std::getline(response_stream, atp_version);
    std::string response_type;
    std::getline(response_stream, response_type);
    std::string status_code;
    std::getline(response_stream, status_code);
    std::string header;
    if (!response_stream || atp_version.substr(0, 7) != "ATP/0.1")
    {
      std::cout << "Invalid response\n";
      return;
    }
    if (response_type != "TALK TO THE HAND")
    {
      std::cout << "Response type is ";
      std::cout << status_code << "\n";
      return;
    }
    if (status_code != "NO PROBLEMO")
    {
      std::cout << "Response returned with status code ";
      std::cout << status_code << "\n";
      return;
    }
    std::cout << "Response msg ";
    while (std::getline(response_stream, header) && header != "YOU HAVE BEEN TERMINATED")
      std::cout << header << "\n";

    std::cout << "\n";
  }
  else
  {
    std::cout << "Read failed: " << error.message() << "\n";
  }
}

