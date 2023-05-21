import logging
import re
import textwrap

from Levenshtein import ratio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def filter_traceback(traceback: str, similarity_threshold=0.6, max_similar_lines=3, runs=2) -> str:
    """
    Filter out similar lines to make traceback more compact.
    :param traceback:
    :param similarity_threshold:
    :param max_similar_lines:
    :param runs: Run multiple times to remove any new duplicate lines after a cleanup
    :return: filtred traceback
    """
    logger.info(f"filtering traceback of length {len(traceback)}")
    traceback = textwrap.dedent(traceback)
    traceback = _remove_file_line_numbers(traceback)
    # remove empty lines
    traceback = '\n'.join(l for l in traceback.splitlines() if l.strip())

    for run in range(runs):
        logger.info(f"run: {run}")
        traceback = _filter_traceback(traceback, similarity_threshold=similarity_threshold,
                                      max_similar_lines=max_similar_lines)
        logger.info(f"filter traceback length {len(traceback)}")

    return traceback


def _filter_traceback(traceback: str, similarity_threshold, max_similar_lines) -> str:
    def _similarity(a, b):
        a = _re_remove_line_nr.sub(")", a)
        b = _re_remove_line_nr.sub(")", b)
        sim = ratio(a, b)
        logger.debug("--")
        logger.debug(a)
        logger.debug(b)
        logger.debug(sim)
        return sim


    out_lines = []
    last_line = ''
    similar_lines_count = 0
    for line in traceback.splitlines(keepends=False):
        # Check if line contains valuable information, similar to the previous line or '... XXX more'
        # Check if we have already included the max number of similar lines
        if last_line and _similarity(last_line, line) > similarity_threshold:
            similar_lines_count += 1
        else:
            similar_lines_count = 1

        if similar_lines_count <= max_similar_lines:
            out_lines.append(line)

        last_line = line
    filtred_traceback = '\n'.join(out_lines)
    logger.debug(f"filter traceback length {len(filtred_traceback)}")

    return filtred_traceback


_re_remove_line_nr = re.compile(r':\d+\)$')


def _remove_file_line_numbers(traceback: str):
    return '\n'.join(_re_remove_line_nr.sub(")", line) for line in traceback.splitlines(keepends=False))

EXAMPLE_TB = """
com.hazelcast.nio.serialization.HazelcastSerializationException: Failed to serialize 'com.acme.schema.v1.Response'
    at com.hazelcast.internal.serialization.impl.SerializationUtil.handleSerializeException(SerializationUtil.java:129)
    at com.hazelcast.internal.serialization.impl.AbstractSerializationService.toBytes(AbstractSerializationService.java:238)
    at com.hazelcast.internal.serialization.impl.AbstractSerializationService.toBytes(AbstractSerializationService.java:214)
    at com.hazelcast.internal.serialization.impl.AbstractSerializationService.toData(AbstractSerializationService.java:199)
    at com.hazelcast.internal.serialization.impl.AbstractSerializationService.toData(AbstractSerializationService.java:154)
    at com.hazelcast.spi.impl.NodeEngineImpl.toData(NodeEngineImpl.java:380)
    at com.hazelcast.spi.impl.AbstractDistributedObject.toData(AbstractDistributedObject.java:78)
    at com.hazelcast.map.impl.proxy.MapProxyImpl.set(MapProxyImpl.java:251)
    at com.hazelcast.map.impl.proxy.MapProxyImpl.set(MapProxyImpl.java:242)
    at com.hazelcast.spring.cache.HazelcastCache.put(HazelcastCache.java:114)
    at com.acme.product.commons.service.CachingSupport.put(CachingSupport.java:55)
    at com.acme.product.httpclient.serviceagent.CachingHttpServiceAgent.lambda$sendWithResponse$0(CachingHttpServiceAgent.java:81)
    at io.reactivex.internal.operators.single.SingleFlatMap$SingleFlatMapCallback.onSuccess(SingleFlatMap.java:76)
    at io.reactivex.internal.operators.single.SingleDoOnSuccess$DoOnSuccess.onSuccess(SingleDoOnSuccess.java:60)
    at io.reactivex.internal.operators.single.SingleResumeNext$ResumeMainSingleObserver.onSuccess(SingleResumeNext.java:65)
    at io.reactivex.internal.operators.single.SingleMap$MapSingleObserver.onSuccess(SingleMap.java:64)
    at io.reactivex.internal.operators.maybe.MaybeToSingle$ToSingleMaybeSubscriber.onSuccess(MaybeToSingle.java:83)
    at io.reactivex.internal.operators.maybe.MaybeCreate$Emitter.onSuccess(MaybeCreate.java:73)
    at org.asynchttpclient.extras.rxjava2.maybe.AbstractMaybeAsyncHandlerBridge.onCompleted(AbstractMaybeAsyncHandlerBridge.java:120)
    at org.asynchttpclient.extras.rxjava2.maybe.AbstractMaybeAsyncHandlerBridge.onCompleted(AbstractMaybeAsyncHandlerBridge.java:52)
    at org.asynchttpclient.netty.NettyResponseFuture.loadContent(NettyResponseFuture.java:222)
    at org.asynchttpclient.netty.NettyResponseFuture.done(NettyResponseFuture.java:257)
    at org.asynchttpclient.netty.handler.AsyncHttpClientHandler.finishUpdate(AsyncHttpClientHandler.java:241)
    at org.asynchttpclient.netty.handler.HttpHandler.handleChunk(HttpHandler.java:113)
    at org.asynchttpclient.netty.handler.HttpHandler.handleRead(HttpHandler.java:142)
    at org.asynchttpclient.netty.handler.AsyncHttpClientHandler.channelRead(AsyncHttpClientHandler.java:78)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:444)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:420)
    at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:412)
    at io.netty.handler.codec.MessageToMessageDecoder.channelRead(MessageToMessageDecoder.java:103)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:444)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:420)
    at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:412)
    at io.netty.channel.CombinedChannelDuplexHandler$DelegatingChannelHandlerContext.fireChannelRead(CombinedChannelDuplexHandler.java:436)
    at io.netty.handler.codec.ByteToMessageDecoder.fireChannelRead(ByteToMessageDecoder.java:346)
    at io.netty.handler.codec.ByteToMessageDecoder.channelRead(ByteToMessageDecoder.java:318)
    at io.netty.channel.CombinedChannelDuplexHandler.channelRead(CombinedChannelDuplexHandler.java:251)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:442)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:420)
    at io.netty.channel.AbstractChannelHandlerContext.fireChannelRead(AbstractChannelHandlerContext.java:412)
    at io.netty.channel.DefaultChannelPipeline$HeadContext.channelRead(DefaultChannelPipeline.java:1410)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:440)
    at io.netty.channel.AbstractChannelHandlerContext.invokeChannelRead(AbstractChannelHandlerContext.java:420)
    at io.netty.channel.DefaultChannelPipeline.fireChannelRead(DefaultChannelPipeline.java:919)
    at io.netty.channel.nio.AbstractNioByteChannel$NioByteUnsafe.read(AbstractNioByteChannel.java:166)
    at io.netty.channel.nio.NioEventLoop.processSelectedKey(NioEventLoop.java:788)
    at io.netty.channel.nio.NioEventLoop.processSelectedKeysOptimized(NioEventLoop.java:724)
    at io.netty.channel.nio.NioEventLoop.processSelectedKeys(NioEventLoop.java:650)
    at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:562)
    at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:997)
    at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
    at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
    at brave.propagation.CurrentTraceContext$1CurrentTraceContextRunnable.run(CurrentTraceContext.java:264)
    at io.netty.util.concurrent.FastThreadLocalRunnable.run(FastThreadLocalRunnable.java:30)
    at java.base/java.lang.Thread.run(Thread.java:833)
Caused by: com.esotericsoftware.kryo.KryoException: java.lang.reflect.InaccessibleObjectException: Unable to make field private transient java.math.BigInteger com.sun.org.apache.xerces.internal.jaxp.datatype.XMLGregorianCalendarImpl.orig_eon accessible: module java.xml does not "opens com.sun.org.apache.xerces.internal.jaxp.datatype" to unnamed module @524d6d96
Serialization trace:
bonusInformation (com.acme.schema.v1.Response$ResponseList)
ResponseList (com.acme.schema.v1.Response)
    at com.esotericsoftware.kryo.serializers.ReflectField.write(ReflectField.java:101)
    at com.esotericsoftware.kryo.serializers.CompatibleFieldSerializer.write(CompatibleFieldSerializer.java:107)
    at com.esotericsoftware.kryo.Kryo.writeObject(Kryo.java:642)
    at com.esotericsoftware.kryo.serializers.ReflectField.write(ReflectField.java:85)
    at com.esotericsoftware.kryo.serializers.CompatibleFieldSerializer.write(CompatibleFieldSerializer.java:107)
    at com.esotericsoftware.kryo.Kryo.writeObject(Kryo.java:627)
    at com.acme.product.commons.config.productCacheConfig$KryoSerializer.write(productCacheConfig.java:346)
    at com.hazelcast.internal.serialization.impl.ByteArraySerializerAdapter.write(ByteArraySerializerAdapter.java:39)
    at com.hazelcast.internal.serialization.impl.AbstractSerializationService.toBytes(AbstractSerializationService.java:235)
    ... 53 common frames omitted
Caused by: java.lang.reflect.InaccessibleObjectException: Unable to make field private transient java.math.BigInteger com.sun.org.apache.xerces.internal.jaxp.datatype.XMLGregorianCalendarImpl.orig_eon accessible: module java.xml does not "opens com.sun.org.apache.xerces.internal.jaxp.datatype" to unnamed module @524d6d96
    at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:354)
    at java.base/java.lang.reflect.AccessibleObject.checkCanSetAccessible(AccessibleObject.java:297)
    at java.base/java.lang.reflect.Field.checkCanSetAccessible(Field.java:178)
    at java.base/java.lang.reflect.Field.setAccessible(Field.java:172)
    at com.esotericsoftware.kryo.serializers.CachedFields.addField(CachedFields.java:123)
    at com.esotericsoftware.kryo.serializers.CachedFields.rebuild(CachedFields.java:99)
    at com.esotericsoftware.kryo.serializers.FieldSerializer.<init>(FieldSerializer.java:82)
    at com.esotericsoftware.kryo.serializers.CompatibleFieldSerializer.<init>(CompatibleFieldSerializer.java:57)
    at com.esotericsoftware.kryo.serializers.CompatibleFieldSerializer.<init>(CompatibleFieldSerializer.java:53)
    at com.acme.product.commons.config.CompatibleFieldAnnotationAwareSerializer.<init>(CompatibleFieldAnnotationAwareSerializer.java:38)
    at com.acme.product.commons.config.CompatibleFieldAnnotationAwareSerializer$Factory.newSerializer(CompatibleFieldAnnotationAwareSerializer.java:82)
    at com.acme.product.commons.config.CompatibleFieldAnnotationAwareSerializer$Factory.newSerializer(CompatibleFieldAnnotationAwareSerializer.java:73)
    at com.esotericsoftware.kryo.Kryo.newDefaultSerializer(Kryo.java:469)
    at com.esotericsoftware.kryo.Kryo.getDefaultSerializer(Kryo.java:454)
    at com.esotericsoftware.kryo.util.DefaultClassResolver.registerImplicit(DefaultClassResolver.java:89)
    at com.esotericsoftware.kryo.Kryo.getRegistration(Kryo.java:581)
    at com.esotericsoftware.kryo.util.DefaultClassResolver.writeClass(DefaultClassResolver.java:112)
    at com.esotericsoftware.kryo.Kryo.writeClass(Kryo.java:613)
    at com.esotericsoftware.kryo.serializers.CompatibleFieldSerializer.write(CompatibleFieldSerializer.java:97)
    at com.esotericsoftware.kryo.Kryo.writeObject(Kryo.java:642)
    at com.esotericsoftware.kryo.serializers.CollectionSerializer.write(CollectionSerializer.java:155)
    at com.esotericsoftware.kryo.serializers.CollectionSerializer.write(CollectionSerializer.java:44)
    at com.esotericsoftware.kryo.Kryo.writeObject(Kryo.java:642)
    at com.esotericsoftware.kryo.serializers.ReflectField.write(ReflectField.java:85)
    ... 61 common frames omitted
"""


if __name__ == '__main__':
    out = filter_traceback(EXAMPLE_TB, similarity_threshold=0.6, max_similar_lines=3)
    print(out)
